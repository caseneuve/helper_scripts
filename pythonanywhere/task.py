import logging

from pythonanywhere.schedule_api import Schedule
from pythonanywhere.snakesay import snakesay

logger = logging.getLogger(name=__name__)


class Task:
    def __init__(self):
        self.command = None
        self.hour = None
        self.minute = None
        self.interval = None
        self.enabled = None
        self.task_id = None
        self.can_enable = None
        self.expiry = None
        self.extend_url = None
        self.logfile = None
        self.printable_time = None
        self.url = None
        self.user = None
        self.schedule = Schedule()

    def __repr__(self):
        enabled = "enabled" if self.enabled else "disabled"
        status = (
            "{} at {}".format(enabled, self.printable_time)
            if self.printable_time
            else "ready to be created"
        )
        num = " <{}>:".format(self.task_id) if self.task_id else ""

        return "{interval} task{num} '{command}' {status}".format(
            interval=self.interval, num=num, command=self.command, status=status
        )

    @classmethod
    def from_id(cls, task_id):
        task = cls()
        specs = task.schedule.get_specs(task_id)
        task.update_specs(specs)
        return task

    @classmethod
    def to_be_created(cls, *, command, minute, hour=None, disabled=False):
        if hour is not None and not (0 <= hour <= 23):
            raise ValueError("Hour has to be in 0..23")
        if not (0 <= minute <= 59):
            raise ValueError("Minute has to be in 0..59")

        task = cls()
        task.command = command
        task.hour = hour
        task.minute = minute
        task.interval = "daily" if hour else "hourly"
        task.enabled = not disabled
        return task

    @classmethod
    def from_specs(cls, specs):
        task = cls()
        task.update_specs(specs)
        return task

    def create_schedule(self):
        params = {
            "command": self.command,
            "enabled": self.enabled,
            "interval": self.interval,
            "minute": self.minute,
        }
        if self.hour:
            params["hour"] = self.hour

        specs = self.schedule.create(params)
        self.update_specs(specs)

        mode = "will" if self.enabled else "may be enabled to"
        msg = (
            "Task '{command}' succesfully created with id {task_id} "
            "and {mode} be run {interval} at {printable_time}"
        ).format(
            command=self.command,
            task_id=self.task_id,
            mode=mode,
            interval=self.interval,
            printable_time=self.printable_time,
        )
        logger.info(snakesay(msg))

    def delete_schedule(self):
        self.schedule.delete(self.task_id)

    def update_specs(self, specs):
        for attr, value in specs.items():
            if attr == "id":
                attr = "task_id"
            setattr(self, attr, value)

    def update_schedule(self, params, porcelain):
        specs = {
            "command": self.command,
            "enabled": self.enabled,
            "interval": self.interval,
            "hour": self.hour,
            "minute": self.minute,
        }
        specs.update(params)

        if specs["interval"] != "daily":
            specs.pop("hour")

        new_specs = self.schedule.update(self.task_id, specs)

        diff = {
            key: (getattr(self, key), new_specs[key])
            for key in specs
            if getattr(self, key) != new_specs[key]
        }

        def make_spec_str(key, old_spec, new_spec):
            return "<{}> from '{}' to '{}'".format(key, old_spec, new_spec)

        updated = [make_spec_str(key, val[0], val[1]) for key, val in diff.items()]

        def make_msg(join_with):
            intro = "Task {} updated:\n".format(self.task_id)
            return "{} {}".format(intro, join_with.join(updated))

        if updated and porcelain:
            logger.info(make_msg(join_with="\n"))
        elif updated:
            logger.info(snakesay(make_msg(join_with=", ")))
        else:
            logger.warning("Nothing to update!")

        self.update_specs(new_specs)


class TaskList:
    def __init__(self):
        self.tasks = [Task.from_specs(specs) for specs in Schedule().get_list()]

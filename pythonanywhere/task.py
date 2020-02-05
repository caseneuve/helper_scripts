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

    @classmethod
    def from_id(cls, task_id):
        task = cls()
        info = task.schedule.get_specs(task_id)
        task.update_specs(info)
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

        info = self.schedule.create(params)
        self.update_specs(info)

    def delete_schedule(self):
        self.schedule.delete(self.task_id)

    def update_specs(self, specs):
        for attr, value in specs.items():
            if attr == "id":
                attr = "task_id"
            setattr(self, attr, value)

    def update_schedule(self, params, logging):
        specs = {
            "command": self.command,
            "enabled": self.enabled,
            "interval": self.interval,
            "hour": self.hour,
            "minute": self.minute,
        }
        specs.update(params)

        new_specs = self.schedule.update(self.task_id, specs)

        # todo: sprawdzić architekturę logowania i skończyć logikę tutaj
        diff = {
            key: (getattr(self, key), new_specs[key])
            for key in specs
            if getattr(self, key) != new_specs[key]
        }

        def make_spec_str(key, old_spec, new_spec):
            return "<{}> from '{}' to '{}'".format(key, old_spec, new_spec)

        updated = [make_spec_str(key, val[0], val[1]) for key, val in diff.items()]
        if updated:
            intro = "Successfully updated:"
            if logging == "porcelain":
                logger.warning(intro)
                for line in updated:
                    logger.warning(line)
            else:
                logger.warning(
                    snakesay("{} {} in task {}".format(intro, ", ".join(updated), self.task_id))
                )
        else:
            logger.warning("Nothing to update!")

        self.update_specs(new_specs)


class TaskList:
    def __init__(self):
        self.tasks = [Task.from_specs(specs) for specs in Schedule().get_list()]

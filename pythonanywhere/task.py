from pythonanywhere.schedule_api import Schedule


class Task:
    def __init__(
        self, *, command=None, hour=None, minute=None, disabled=None, task_id=None
    ):
        self.command = command
        self.hour = hour
        self.minute = minute
        self.interval = "daily" if hour else "hourly" if not task_id else None
        self.enabled = not disabled if not task_id else None
        self.task_id = task_id
        self.can_enable = None
        self.expiry = None
        self.extend_url = None
        self.logfile = None
        self.printable_time = None
        self.url = None
        self.user = None
        self.schedule = Schedule()

        if task_id:
            info = self.schedule.get_specs(task_id)
            self.update_specs(info)

    def create_schedule(self):
        params = {
            "command": self.command,
            "enabled": self.enabled,
            "hour": self.hour,
            "interval": self.interval,
            "minute": self.minute,
        }
        info = self.schedule.create(params)
        self.update_specs(info)

    def delete_schedule(self):
        self.schedule.delete(self.task_id)

    def update_specs(self, specs):
        for attr, value in specs.items():
            setattr(self, attr, value)

import getpass

from pythonanywhere.api import call_api, get_api_endpoint
from pythonanywhere.schedule_api import Schedule
from pythonanywhere.snakesay import snakesay


class Task:
    def __init__(self, command, hour, minute, disabled):
        self.command = command
        self.hour = hour
        self.minute = minute
        self.interval = "daily" if hour else "hourly"
        self.enabled = not disabled
        self.can_enable = None
        self.expiry = None
        self.extend_url = None
        self.logfile = None
        self.printable_time = None
        self.task_id = None
        self.url = None
        self.schedule = Schedule()

    def create_schedule(self):
        params = {
            "command": self.command,
            "enable": self.enabled,
            "hour": self.hour,
            "interval": self.interval,
            "minute": self.minute,
        }
        result = self.schedule.create(params)

        for attr, value in result.items():
            if not getattr(self, attr):
                setattr(self, attr, value)

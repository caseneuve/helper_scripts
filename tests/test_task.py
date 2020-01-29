import getpass
import json
from unittest.mock import Mock, call, patch

import pytest
import responses

from pythonanywhere.api import get_api_endpoint
from pythonanywhere.task import Task


class TestTask:
    def test_daily_enabled(self):
        task = Task("myscript.py", 8, 10, False)
        assert task.command == "myscript.py"
        assert task.hour == 8
        assert task.minute == 10
        assert task.interval == "daily"
        assert task.enabled is True

    def test_hourly_disabled(self):
        task = Task("myscript.py", None, 10, True)
        assert task.command == "myscript.py"
        assert task.hour == None
        assert task.minute == 10
        assert task.interval == "hourly"
        assert task.enabled is False

    def test_creates_daily_task(self, api_token, api_responses):
        username = getpass.getuser()
        url = get_api_endpoint().format(username=username, flavor="schedule")
        task_specs = {
            "can_enable": False,
            "command": "echo foo",
            "enabled": True,
            "expiry": None,
            "extend_url": "/user/{username}/schedule/task/123/extend".format(
                username=username
            ),
            "hour": 16,
            "id": 123,
            "interval": "daily",
            "logfile": "/user/{username}/files/var/log/tasklog-126708-daily-at-1600-echo_foo.log",
            "minute": 0,
            "printable_time": "16:00",
            "url": "/api/v0/user/{username}/schedule/123".format(username=username),
        }

        api_responses.add(
            responses.POST, url=url, status=201, body=json.dumps(task_specs),
        )

        task = Task("echo foo", 16, 0, False)
        task.create_schedule()

        task_specs["task_id"] = task_specs.pop("id")

        for attr, value in task_specs.items():
            assert getattr(task, attr) == value

import getpass
import json
from unittest.mock import Mock, call, patch

import pytest
import responses

from pythonanywhere.api import get_api_endpoint
from pythonanywhere.task import Task


@pytest.mark.tasks
class TestTask:
    def test_new_daily_enabled(self):
        task = Task(command="myscript.py", hour=8, minute=10, disabled=False)
        assert task.command == "myscript.py"
        assert task.hour == 8
        assert task.minute == 10
        assert task.interval == "daily"
        assert task.enabled is True

    def test_new_hourly_disabled(self):
        task = Task(command="myscript.py", hour=None, minute=10, disabled=True)
        assert task.command == "myscript.py"
        assert task.hour == None
        assert task.minute == 10
        assert task.interval == "hourly"
        assert task.enabled is False

    def test_old_task(self):
        task = Task(task_id=42)
        assert task.task_id == 42
        assert task.interval == None
        assert task.enabled == None

    def test_creates_daily_task(self, api_token, api_responses, mocker):
        mock_create = mocker.patch("pythonanywhere.schedule_api.Schedule.create")
        username = getpass.getuser()
        task_specs = {
            "can_enable": False,
            "command": "echo foo",
            "enabled": True,
            "expiry": None,
            "extend_url": "/user/{username}/schedule/task/123/extend".format(
                username=username
            ),
            "hour": 16,
            "task_id": 123,
            "interval": "daily",
            "logfile": "/user/{username}/files/var/log/tasklog-126708-daily-at-1600-echo_foo.log",
            "minute": 0,
            "printable_time": "16:00",
            "url": "/api/v0/user/{username}/schedule/123".format(username=username),
            "user": username,
        }
        mock_create.return_value = task_specs
        task = Task(command="echo foo", hour=16, minute=0, disabled=False)

        task.create_schedule()

        for attr, value in task_specs.items():
            assert getattr(task, attr) == value
        assert mock_create.call_count == 1

    def test_calls_schedule_delete(self, mocker):
        mock_delete = mocker.patch("pythonanywhere.schedule_api.Schedule.delete")

        Task(task_id=42).delete_schedule()

        assert mock_delete.call_args == call(42)

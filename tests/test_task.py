import getpass
import json
from unittest.mock import Mock, call, patch

import pytest
import responses

from pythonanywhere.api import get_api_endpoint
from pythonanywhere.task import Task, TaskList

username = getpass.getuser()
example_specs = {
    "can_enable": False,
    "command": "echo foo",
    "enabled": True,
    "expiry": None,
    "extend_url": "/user/{username}/schedule/task/42/extend".format(username=username),
    "hour": 16,
    "id": 42,
    "interval": "daily",
    "logfile": "/user/{username}/files/var/log/tasklog-126708-daily-at-1600-echo_foo.log",
    "minute": 0,
    "printable_time": "16:00",
    "url": "/api/v0/user/{username}/schedule/42".format(username=username),
    "user": username,
}


@pytest.mark.tasks
class TestTaskToBeCreated:
    def test_instances_new_daily_enabled(self):
        task = Task.to_be_created(
            command="myscript.py", hour=8, minute=10, disabled=False
        )
        assert task.command == "myscript.py"
        assert task.hour == 8
        assert task.minute == 10
        assert task.interval == "daily"
        assert task.enabled is True

    def test_instances_new_hourly_disabled(self, mocker):
        task = Task.to_be_created(
            command="myscript.py", hour=None, minute=10, disabled=True
        )
        assert task.command == "myscript.py"
        assert task.hour == None
        assert task.minute == 10
        assert task.interval == "hourly"
        assert task.enabled is False


@pytest.mark.tasks
class TestTaskFromId:
    def test_updates_specs(self, mocker):
        mock_get_specs = mocker.patch("pythonanywhere.schedule_api.Schedule.get_specs")
        specs = dict(**example_specs)
        specs["task_id"] = specs.pop("id")
        mock_get_specs.return_value = example_specs
        task = Task.from_id(task_id=42)
        assert task.can_enable == False
        assert task.command == "echo foo"
        assert task.enabled == True
        assert task.expiry == None
        assert task.extend_url == "/user/{username}/schedule/task/42/extend".format(
            username=username
        )
        assert task.hour == 16
        assert task.task_id == 42
        assert task.interval == "daily"
        assert (
            task.logfile
            == "/user/{username}/files/var/log/tasklog-126708-daily-at-1600-echo_foo.log"
        )
        assert task.minute == 0
        assert task.printable_time == "16:00"
        assert task.url == "/api/v0/user/{username}/schedule/42".format(
            username=username
        )
        assert task.user == username


@pytest.mark.tasks
class TestTaskCreateSchedule:
    def test_creates_daily_task(self, mocker):
        mock_create = mocker.patch("pythonanywhere.schedule_api.Schedule.create")
        mock_create.return_value = example_specs
        mock_update_specs = mocker.patch("pythonanywhere.task.Task.update_specs")
        task = Task.to_be_created(command="echo foo", hour=16, minute=0, disabled=False)

        task.create_schedule()

        assert mock_update_specs.call_args == call(example_specs)
        assert mock_create.call_count == 1
        assert mock_create.call_args == call(
            {
                "command": "echo foo",
                "hour": 16,
                "minute": 0,
                "enabled": True,
                "interval": "daily",
            }
        )


@pytest.mark.tasks
class TestTaskDeleteSchedule:
    def test_calls_schedule_delete(self, mocker):
        mock_delete = mocker.patch("pythonanywhere.schedule_api.Schedule.delete")
        mock_get_specs = mocker.patch("pythonanywhere.schedule_api.Schedule.get_specs")
        mock_get_specs.return_value = example_specs

        Task.from_id(task_id=42).delete_schedule()

        assert mock_delete.call_args == call(42)

    def test_raises_when_to_be_created_gets_wrong_hour(self):
        with pytest.raises(ValueError) as e:
            Task.to_be_created(command="echo foo", hour=25, minute=1)
        assert str(e.value) == "Hour has to be in 0..23"

    def test_raises_when_to_be_created_gets_wrong_minute(self):
        with pytest.raises(ValueError) as e:
            Task.to_be_created(command="echo foo", hour=12, minute=78)
        assert str(e.value) == "Minute has to be in 0..59"


@pytest.mark.tasks
class TestTaskUpdateSchedule:
    def test_calls_schedule_update(self, mocker):
        params = {"enabled": True}
        mock_schedule_update = mocker.patch(
            "pythonanywhere.schedule_api.Schedule.update"
        )
        mock_update_specs = mocker.patch("pythonanywhere.schedule_api.Schedule.update")
        mock_get_specs = mocker.patch("pythonanywhere.schedule_api.Schedule.get_specs")
        mock_update_specs.return_value = {
            "command": "echo foo",
            "enabled": False,
            "interval": "daily",
            "hour": 10,
            "minute": 23,
        }

        Task.from_id(task_id=42).update_schedule(params)

        assert mock_update_specs.call_args == call(
            None,
            {
                "command": None,
                "enabled": True,
                "interval": None,
                "minute": None,
                "hour": None,
            },
        )


@pytest.mark.tasks
class TestTaskList:
    def test_pass(self, mocker):
        mock_get_list = mocker.patch("pythonanywhere.schedule_api.Schedule.get_list")
        mock_get_list.return_value = [example_specs]
        mock_from_specs = mocker.patch("pythonanywhere.task.Task.from_specs")

        task_list = TaskList().tasks

        assert mock_from_specs.call_args == call(example_specs)
        assert mock_get_list.call_count == 1

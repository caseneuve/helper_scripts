import getpass
from unittest.mock import call

import pytest
from scripts.pa_get_scheduled_tasks_list import main

from pythonanywhere.task import Task


@pytest.fixture
def example_tasks_list():
    username = getpass.getuser()
    specs1 = {
        "can_enable": False,
        "command": "echo foo",
        "enabled": True,
        "expiry": None,
        "extend_url": "/user/{}/schedule/task/42/extend".format(username),
        "hour": 16,
        "id": 42,
        "interval": "daily",
        "logfile": "/user/{username}/files/var/log/tasklog-126708-daily-at-1600-echo_foo.log",
        "minute": 0,
        "printable_time": "16:00",
        "url": "/api/v0/user/{}/schedule/42".format(username),
        "user": username,
    }
    specs2 = {**specs1}
    specs2.update({"command": "echo bar", "hour": 17, "minute": 43, "printable_time": "17:43"})
    yield [specs1, specs2]


@pytest.mark.tasks
def test_logs_task_list_as_table(example_tasks_list, mocker):
    tasks = [Task._from_specs(specs) for specs in example_tasks_list]
    mock_TaskList = mocker.patch("scripts.pa_get_scheduled_tasks_list.TaskList")
    mock_TaskList.return_value.tasks = tasks
    mock_tabulate = mocker.patch("scripts.pa_get_scheduled_tasks_list.tabulate")
    mock_logger = mocker.patch("scripts.pa_get_scheduled_tasks_list.get_logger")

    main(tablefmt="orgtbl")

    headers = "id", "interval", "at", "enabled", "command"
    attrs = "task_id", "interval", "printable_time", "enabled", "command"
    table = [[getattr(task, attr) for attr in attrs] for task in tasks]

    assert mock_TaskList.call_count == 1
    assert mock_tabulate.call_args == call(table, headers, tablefmt="orgtbl")
    assert mock_logger.call_args == call(set_info=True)
    assert mock_logger.return_value.info.call_count == 1

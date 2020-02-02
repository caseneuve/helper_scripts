import getpass
from unittest.mock import call

import pytest
from scripts.pa_get_scheduled_tasks_list import main
from pythonanywhere.task import Task

username = getpass.getuser()
example_specs = [
    {
        "can_enable": False,
        "command": "echo foo",
        "enabled": True,
        "expiry": None,
        "extend_url": "/user/{username}/schedule/task/42/extend".format(
            username=username
        ),
        "hour": 16,
        "id": 42,
        "interval": "daily",
        "logfile": "/user/{username}/files/var/log/tasklog-126708-daily-at-1600-echo_foo.log",
        "minute": 0,
        "printable_time": "16:00",
        "url": "/api/v0/user/{username}/schedule/42".format(username=username),
        "user": username,
    },
    {
        "can_enable": False,
        "command": "echo bar",
        "enabled": False,
        "expiry": None,
        "extend_url": "/user/{username}/schedule/task/43/extend".format(
            username=username
        ),
        "hour": 17,
        "id": 43,
        "interval": "daily",
        "logfile": "/user/{username}/files/var/log/tasklog-126709-daily-at-1710-echo_bar.log",
        "minute": 10,
        "printable_time": "17:10",
        "url": "/api/v0/user/{username}/schedule/43".format(username=username),
        "user": username,
    },
]


@pytest.mark.tasks
@pytest.mark.dev
def test_calls_all_stuff_in_right_order(mocker):
    mock_TaskList = mocker.patch("scripts.pa_get_scheduled_tasks_list.TaskList")
    mock_TaskList.return_value.tasks = [
        Task.from_specs(specs) for specs in example_specs
    ]
    mock_tabulate = mocker.patch("scripts.pa_get_scheduled_tasks_list.tabulate")

    main(fmt="orgtbl", columns=None)

    headers = "id", "interval", "at", "enabled", "command"
    attrs = "task_id", "interval", "printable_time", "enabled", "command"
    tasks = [Task.from_specs(specs) for specs in example_specs]
    table = [[getattr(task, attr) for attr in attrs] for task in tasks]
    assert mock_TaskList.call_count == 1
    assert mock_tabulate.call_args == call(table, headers, tablefmt="orgtbl")

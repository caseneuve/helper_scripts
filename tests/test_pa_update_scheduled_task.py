import getpass
from unittest.mock import call

import pytest
from scripts.pa_update_scheduled_task import main

specs = {
    "can_enable": False,
    "command": "echo foo",
    "enabled": False,
    "hour": 10,
    "interval": "daily",
    "logfile": "/user/{}/files/foo".format(getpass.getuser()),
    "minute": 23,
    "printable_time": "10:23",
    "task_id": 42,
    "username": getpass.getuser(),
}


@pytest.fixture()
def args():
    yield {
        "command": None,
        "hour": None,
        "minute": None,
        "disable": None,
        "enable": None,
        "toggle": None,
        "quiet": None,
        "porcelain": None,
    }


@pytest.fixture()
def task_from_id(mocker):
    task = mocker.patch("scripts.pa_update_scheduled_task.Task.from_id")
    for spec, value in specs.items():
        setattr(task.return_value, spec, value)
    yield task


# FIXME: NIE DZIAŁA!
@pytest.mark.tasks
@pytest.mark.now
def test_enables_task(task_from_id, args, mocker):
    mock_schedule_update = mocker.patch("pythonanywhere.schedule_api.Schedule.update")
    mock_schedule_update.return_value.result_code = 200
    mock_schedule_update.return_value.json.return_value = specs.update({"enabled": True})
    args.update({"enable": True})

    main(42, **args)

    print(mock_schedule_update.call_args)
    # assert mock_schedule_update.call_args == call(args)
    # print(task_from_id.return_value.update_schedule.call_args)
    assert task_from_id.return_value.update_schedule.call_count == 1

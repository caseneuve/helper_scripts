import getpass
from unittest.mock import call

import pytest
from scripts.pa_get_scheduled_task_specs import main


@pytest.fixture()
def args():
    yield {
        "command": None,
        "enabled": None,
        "hour": None,
        "interval": None,
        "logfile": None,
        "minute": None,
        "printable_time": None,
        "snake": None,
    }


@pytest.fixture()
def task_from_id(mocker):
    specs = {
        "can_enable": False,
        "command": "echo foo",
        "enabled": True,
        "hour": 10,
        "interval": "daily",
        "logfile": "/user/{}/files/foo".format(getpass.getuser()),
        "minute": 23,
        "printable_time": "10:23",
        "task_id": 42,
        "username": getpass.getuser(),
    }
    task = mocker.patch("scripts.pa_get_scheduled_task_specs.Task.from_id")
    for spec, value in specs.items():
        setattr(task.return_value, spec, value)
    yield task


@pytest.mark.tasks
class TestGetScheduledTaskSpecs:
    def test_prints_all_specs_using_tabulate(self, task_from_id, args, mocker):
        mock_tabulate = mocker.patch("scripts.pa_get_scheduled_task_specs.tabulate")

        main(42, **args)

        assert task_from_id.call_args == call(42)
        assert mock_tabulate.call_args == call(
            [
                ["command", "echo foo"],
                ["enabled", True],
                ["hour", 10],
                ["interval", "daily"],
                ["logfile", "/user/piotr/files/foo"],
                ["minute", 23],
                ["printable_time", "10:23"],
            ],
            tablefmt="simple",
        )

    def test_prints_all_specs_using_snakesay(self, task_from_id, args, mocker):
        args.update({"snake": True})
        mock_snakesay = mocker.patch("scripts.pa_get_scheduled_task_specs.snakesay")

        main(42, **args)

        assert task_from_id.call_args == call(42)
        assert mock_snakesay.call_args == call(
            "Task 42 specs: <command>: echo foo, <enabled>: True, <hour>: 10, <interval>: daily, "
            "<logfile>: /user/piotr/files/foo, <minute>: 23, <printable_time>: 10:23"
        )

    def test_prints_one_spec(self, task_from_id, args, mocker):
        args.update({"command": True})
        mock_tabulate = mocker.patch("scripts.pa_get_scheduled_task_specs.tabulate")

        main(42, **args)

        assert task_from_id.call_args == call(42)
        assert mock_tabulate.call_args == call([["command", "echo foo"]], tablefmt="simple")
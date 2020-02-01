import getpass
from unittest.mock import call

import pytest
from scripts.pa_get_scheduled_task_log import main


@pytest.mark.tasks
def test_calls_all_stuff_in_right_order(mocker):
    mock_task_from_id = mocker.patch("scripts.pa_get_scheduled_task_log.Task.from_id")
    mock_task_from_id.return_value.logfile = "/user/{username}/files/foo".format(
        username=getpass.getuser()
    )
    mock_print = mocker.patch("builtins.print")

    main(42)

    assert mock_task_from_id.call_args == call(task_id=42)
    assert mock_print.call_args == call("/foo")

from unittest.mock import call

import pytest
from scripts.pa_create_scheduled_task import main


@pytest.mark.tasks
def test_calls_all_stuff_in_right_order(mocker):
    mock_Task = mocker.patch("scripts.pa_create_scheduled_task.Task")

    main("echo foo", 8, 10, False)

    assert mock_Task.call_args == call("echo foo", 8, 10, False)
    assert mock_Task.return_value.method_calls == [call.create_schedule()]

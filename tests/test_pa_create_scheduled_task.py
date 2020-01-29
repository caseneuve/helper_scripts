from unittest.mock import call, patch

import pytest

from scripts.pa_create_scheduled_task import main


def test_calls_all_stuff_in_right_order():
    with patch("scripts.pa_create_scheduled_task.Task") as mock_Task:
        main("echo foo", 8, 10, False)
    assert mock_Task.call_args == call("echo foo", 8, 10, False)
    assert mock_Task.return_value.method_calls == [call.create_schedule()]

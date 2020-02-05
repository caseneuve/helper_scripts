from unittest.mock import call

import pytest
from scripts.pa_delete_scheduled_task import main


@pytest.mark.tasks
def test_calls_all_stuff_in_right_order(mocker):
    mock_Task_from_id = mocker.patch("scripts.pa_delete_scheduled_task.Task.from_id")

    main(task_id=42)

    assert mock_Task_from_id.call_args == call(42)
    assert mock_Task_from_id.return_value.method_calls == [call.delete_schedule()]

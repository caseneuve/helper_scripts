from unittest.mock import call

from scripts.pa_delete_scheduled_task import main


def test_calls_all_stuff_in_right_order(mocker):
    mock_Task = mocker.patch("scripts.pa_delete_scheduled_task.Task")

    main(42)

    assert mock_Task.call_args == call(task_id=42)
    assert mock_Task.return_value.method_calls == [call.delete_schedule()]

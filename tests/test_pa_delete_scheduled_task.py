from unittest.mock import call

import pytest
from scripts.pa_delete_scheduled_task import main


@pytest.mark.tasks
class TestDeleteScheduledTask:
    def test_deletes_task(self, mocker):
        mock_Task_from_id = mocker.patch("scripts.pa_delete_scheduled_task.get_task_from_id")

        main(task_id=42)

        assert mock_Task_from_id.call_args == call(42)
        assert mock_Task_from_id.return_value.method_calls == [call.delete_schedule()]

    def test_exits_when_attempt_to_delete_non_existing_task(self, mocker):
        mock_get_task = mocker.patch("pythonanywhere.scripts_commons.get_task_from_id")
        mock_from_id = mocker.patch("pythonanywhere.task.Task.from_id")
        mock_from_id.side_effect = Exception("error")
        mock_logger = mocker.patch("pythonanywhere.scripts_commons.logger.warning")
        mock_exit = mocker.patch("pythonanywhere.scripts_commons.sys.exit")

        with pytest.raises(Exception):
            main(task_id=999)

        assert mock_exit.call_count == 1
        assert mock_logger.call_args == call("\n< error >\n   \\\n    ~<:>>>>>>>>>")

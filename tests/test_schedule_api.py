import getpass
import json
from unittest.mock import call

import pytest
import responses

from pythonanywhere.api import get_api_endpoint
from pythonanywhere.schedule_api import Schedule


@pytest.mark.tasks
class TestScheduleCreate:
    def test_checks_params(self):
        pass

    def test_creates_daily_task(self, api_token, api_responses):
        username = getpass.getuser()
        url = get_api_endpoint().format(username=username, flavor="schedule")
        params = {
            "command": "echo foo",
            "enabled": True,
            "hour": 16,
            "interval": "daily",
            "minute": 0,
        }
        task_specs = {
            "can_enable": False,
            "command": "echo foo",
            "enabled": True,
            "expiry": None,
            "extend_url": "/user/{username}/schedule/task/123/extend".format(
                username=username
            ),
            "hour": 16,
            "id": 123,
            "interval": "daily",
            "logfile": "/user/{username}/files/var/log/tasklog-126708-daily-at-1600-echo_foo.log",
            "minute": 0,
            "printable_time": "16:00",
            "url": "/api/v0/user/{username}/schedule/123".format(username=username),
            "user": username,
        }
        api_responses.add(
            responses.POST, url=url, status=201, body=json.dumps(task_specs),
        )

        result = Schedule().create(params)

        task_specs["task_id"] = task_specs.pop("id")

        assert result == task_specs


class TestScheduleDelete:
    def test_deletes_task(self, api_token, api_responses, mocker):
        mock_snakesay = mocker.patch("pythonanywhere.schedule_api.snakesay")
        username = getpass.getuser()
        url = get_api_endpoint().format(username=username, flavor="schedule") + "42/"
        api_responses.add(responses.DELETE, url=url, status=204)

        Schedule().delete(42)

        post = api_responses.calls[0]
        assert post.request.url == url
        assert post.request.body == None
        assert mock_snakesay.call_args == call("Task 42 deleted!")

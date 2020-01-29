import getpass
import json
from pythonanywhere.api import call_api, get_api_endpoint
from pythonanywhere.snakesay import snakesay


class Schedule:
    def __init__(self):
        self.base_url = get_api_endpoint().format(
            username=getpass.getuser(), flavor="schedule"
        )

    def create(self, params):
        result = call_api(self.base_url, "POST", json=json.dumps(params))

        if result.status_code == 201:
            json_ = result.json()
            json_["task_id"] = json_.pop("id")
            print(
                snakesay(
                    "Task '{command}' succesfully created with id {id_} "
                    "and will be run {interval} at {printable_time}".format(
                        command=json_["command"],
                        id_=json_["task_id"],
                        interval=json_["interval"],
                        printable_time=json_["printable_time"],
                    )
                )
            )
            return json_

        if not result.ok:
            raise Exception(
                "POST to set new task via API failed,"
                "got {result}:{result_text}".format(
                    result=result, result_text=result.text
                )
            )

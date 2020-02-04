import getpass

from pythonanywhere.api import call_api, get_api_endpoint
from pythonanywhere.snakesay import snakesay


class Schedule:
    def __init__(self):
        self.base_url = get_api_endpoint().format(
            username=getpass.getuser(), flavor="schedule"
        )

    def create(self, params):
        result = call_api(self.base_url, "POST", json=params)

        if result.status_code == 201:
            specs = result.json()
            print(
                snakesay(
                    "Task '{command}' succesfully created with id {id_} "
                    "and will be run {interval} at {printable_time}".format(
                        command=specs["command"],
                        id_=specs["id"],
                        interval=specs["interval"],
                        printable_time=specs["printable_time"],
                    )
                )
            )
            return specs

        if not result.ok:
            raise Exception(
                "POST to set new task via API failed, got {result}: "
                "{result_text}".format(result=result, result_text=result.text)
            )

    def delete(self, task_id):
        result = call_api(
            "{base_url}{task_id}/".format(base_url=self.base_url, task_id=task_id),
            "DELETE",
        )

        if result.status_code == 204:
            print(snakesay("Task {task_id} deleted!".format(task_id=task_id)))

        if not result.ok:
            raise Exception(
                "DELETE via API on task {task_id} failed, got {result}: "
                "{result_text}".format(
                    task_id=task_id, result=result, result_text=result.text
                )
            )

    def get_specs(self, task_id):
        result = call_api(
            "{base_url}{task_id}/".format(base_url=self.base_url, task_id=task_id),
            "GET",
        )
        if result.status_code == 200:
            return result.json()
        else:
            raise Exception(
                "Could not get task with id {task_id}. Got result {result}: {content}".format(
                    task_id=task_id, result=result, content=str(result.content)
                )
            )

    def get_list(self):
        result = call_api("{base_url}".format(base_url=self.base_url), "GET")
        return result.json()

    def update(self, task_id, params):
        result = call_api(
            "{base_url}{task_id}/".format(base_url=self.base_url), "PATCH", json=params
        )
        if result.status_code == 200:
            return result.json()
        else:
            raise Exception(
                "Could not update task {task_id}. Got {result}: {content}".format(
                    task_id=task_id, result=result, content=str(result.content)
                )
            )

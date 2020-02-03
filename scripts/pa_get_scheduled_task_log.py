#!/usr/bin/python3.5
"""Get current scheduled task's log file by task id.

Usage:
  pa_get_scheduled_task_log.py <id>

Options:
  -h --help                      Print this message

Note:
  Task <id> may be found using pa_get_scheduled_tasks_list.py script.
"""

import getpass

from docopt import docopt
from schema import And, Schema, Use

from pythonanywhere.scripts_commons import validate_user_input
from pythonanywhere.task import Task


def main(task_id):
    filename = Task.from_id(task_id=task_id).logfile

    # hack to get user path instead of server path:
    filename = filename.replace(
        "/user/{username}/files".format(username=getpass.getuser()), ""
    )

    print(filename)


if __name__ == "__main__":
    schema = Schema({"<id>": And(Use(int), error="<id> should be an integer")})
    arguments = validate_user_input(docopt(__doc__), schema)

    main(int(arguments["<id>"]))

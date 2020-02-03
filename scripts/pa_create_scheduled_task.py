#!/usr/bin/python3.5
"""Create a new scheduled task.

Usage:
  pa_create_scheduled_task.py --command <command> [--hour=<hour>] --minute=<minute> [--disabled]

Options:
  -h --help                      Print this message
  -c --command=<command>         Shell command to be scheduled
  -o --hour=<hour>               Sets the task to be performed daily on the specified hour
                                 (otherwise the task will be run hourly)
  -m --minute=<minute>           Minute on which the task will be executed
  -d --disabled                  Create disabled task (by default tasks are enabled)

Example:
  Create a daily task to be run at 13:15:

    pa_create_scheduled_task.py --command "echo foo" --hour 13 --minute 15

  Create an inactive hourly task to be run 27 minutes past every hour:

    pa_create_scheduled_task.py --command "echo bar" --minute 27 --disabled
"""

from docopt import docopt
from schema import And, Or, Schema, SchemaError, Use

from pythonanywhere.scripts_commons import validate_user_input
from pythonanywhere.task import Task


def main(command, hour, minute, disabled):
    hour = int(hour) if hour is not None else None
    task = Task.to_be_created(
        command=command, hour=hour, minute=int(minute), disabled=disabled
    )
    task.create_schedule()


if __name__ == "__main__":
    schema = Schema(
        {
            "--command": str,
            "--hour": Or(
                None,
                And(Use(int), lambda h: 0 <= h <= 23),
                error="--hour has to be in 0..23",
            ),
            "--minute": And(
                Use(int), lambda m: 0 <= m <= 59, error="--minute has to be in 0..59"
            ),
            "--disabled": Or(None, bool),
        }
    )
    arguments = validate_user_input(docopt(__doc__), schema)

    main(
        arguments["--command"],
        arguments["--hour"],
        arguments["--minute"],
        arguments["--disabled"],
    )

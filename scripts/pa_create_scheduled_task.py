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

from pythonanywhere.scripts_commons import ScriptSchema, get_logger
from pythonanywhere.task import Task


def main(command, hour, minute, disabled):
    get_logger(set_info=True)
    hour = int(hour) if hour is not None else None
    task = Task.to_be_created(command=command, hour=hour, minute=int(minute), disabled=disabled)
    task.create_schedule()


if __name__ == "__main__":
    schema = ScriptSchema(
        {
            "--command": str,
            "--hour": ScriptSchema.hour,
            "--minute": ScriptSchema.minute,
            "--disabled": ScriptSchema.boolean,
        }
    )
    arguments = schema.validate_user_input(docopt(__doc__))

    main(**arguments)

# #!/usr/bin/python3.5
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
"""

from docopt import docopt

from pythonanywhere.task import Task


def main(command, hour, minute, disabled):
    task = Task(command, hour, minute, disabled)
    task.create_schedule()


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main(
        arguments["--command"],
        int(arguments["--hour"]),
        int(arguments["--minute"]),
        arguments["--disabled"],
    )

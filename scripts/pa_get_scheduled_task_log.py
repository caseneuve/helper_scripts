#!/usr/bin/python3.5
"""Get current scheduled task log file by task.

Usage:
  pa_get_scheduled_task_log.py <id>

Options:
  -h --help                      Print this message
"""

from docopt import docopt

from pythonanywhere.task import Task


def main(task_id):
    print(Task(task_id=task_id).logfile)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main(int(arguments["<id>"]))

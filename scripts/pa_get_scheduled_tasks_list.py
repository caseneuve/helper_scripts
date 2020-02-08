#!/usr/bin/python3.5
"""Get list of user's scheduled tasks as a table with columns:
id, interval, at (hour:minute/minute past), enabled, command.

Usage:
  pa_get_scheduled_tasks_list.py [--format=<format>]

Options:
  -h --help                      Print this message
  -f --format=<format>           Table format supported by tabulate
                                 (defaults to 'simple')"""

from docopt import docopt
from tabulate import tabulate

from pythonanywhere.scripts_commons import ScriptSchema, get_logger
from pythonanywhere.task import TaskList


def main(tablefmt):
    logger = get_logger(set_info=True)
    headers = "id", "interval", "at", "enabled", "command"
    attrs = "task_id", "interval", "printable_time", "enabled", "command"
    table = [[getattr(task, attr) for attr in attrs] for task in TaskList().tasks]
    logger.info(tabulate(table, headers, tablefmt=tablefmt))


if __name__ == "__main__":
    schema = ScriptSchema({"--format": ScriptSchema.tabulate_format})
    argument = schema.validate_user_input(docopt(__doc__))

    main(argument.get("format", "simple"))

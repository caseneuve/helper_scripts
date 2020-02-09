#!/usr/bin/python3.5
"""Get list of user's scheduled tasks as a table with columns:
id, interval, at (hour:minute/minute past), enabled, command.

Usage:
  pa_get_scheduled_tasks_list.py [--format TABLEFMT]

Options:
  -h, --help                  Prints this message
  -f, --format TABLEFMT       Sets table format supported by tabulate
                              (defaults to 'simple')"""

from docopt import docopt
from tabulate import tabulate

from pythonanywhere.scripts_commons import ScriptSchema, get_logger
from pythonanywhere.snakesay import snakesay
from pythonanywhere.task import TaskList


def main(tablefmt):
    logger = get_logger(set_info=True)
    headers = "id", "interval", "at", "status", "command"
    attrs = "task_id", "interval", "printable_time", "enabled", "command"

    def convert(task, attr):
        value = getattr(task, attr)
        if attr == "enabled":
            value = "enabled" if value else "disabled"
        return value

    table = [[convert(task, attr) for attr in attrs] for task in TaskList().tasks]
    msg = tabulate(table, headers, tablefmt=tablefmt) if table else snakesay("No active tasks")
    logger.info(msg)


if __name__ == "__main__":
    schema = ScriptSchema({"--format": ScriptSchema.tabulate_format})
    argument = schema.validate_user_input(docopt(__doc__))

    main(argument.get("format", "simple"))

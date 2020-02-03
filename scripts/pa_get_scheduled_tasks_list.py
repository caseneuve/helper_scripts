#!/usr/bin/python3.5
"""Get list of user's scheduled tasks as a table with default columns:
id, interval, at (hour:minute/minute past), enabled, command.

Usage:
  pa_get_scheduled_tasks_list.py [--format=<format>] [--columns=<comma_separated_cols>] [--listfmt]

Options:
  -h --help                      Print this message
  -f --format=<format>           Table format supported by tabulate
                                 (defaults to 'simple')
  -c --columns=<columns>         Comma separated columns to display
                                 (defaults to all)
"""

import getpass
import sys

from docopt import docopt
from schema import And, Or, Schema, SchemaError, Use
from tabulate import tabulate

from pythonanywhere.scripts_commons import validate_user_input
from pythonanywhere.task import TaskList

headers = "id", "interval", "at", "enabled", "command"
formats = [
    "plain",
    "simple",
    "github",
    "grid",
    "fancy_grid",
    "pipe",
    "orgtbl",
    "jira",
    "presto",
    "psql",
    "rst",
    "mediawiki",
    "moinmoin",
    "youtrack",
    "html",
    "latex",
    "latex_raw",
    "latex_booktabs",
    "textile",
]


def main(fmt):
    attrs = "task_id", "interval", "printable_time", "enabled", "command"
    table = [[getattr(task, attr) for attr in attrs] for task in TaskList().tasks]
    print(tabulate(table, headers, tablefmt=fmt))


if __name__ == "__main__":
    schema = Schema(
        {
            "--format": Or(
                None,
                And(str, lambda f: f in formats),
                error="--format should match one of: {}".format(", ".join(formats)),
            )
        }
    )
    arguments = validate_user_input(docopt(__doc__), schema)

    main(arguments.get("--format", "simple"),)

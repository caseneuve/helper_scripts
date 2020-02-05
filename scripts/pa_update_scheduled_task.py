#!/usr/bin/python3.5
"""Update a scheduled task. Note that logfile name will change after updating the task
but it won't be created until first execution of the task.

Usage:
  pa_update_scheduled_task.py <id> [--command=CMD] [--hour=HOUR] [--minute=MINUTE]
                                   [--disable | --enable | --toggle]
                                   [--quiet | --porcelain]

Options:
  -h --help                      Print this message
  -c --command=CMD               Changes command to CMD (multiword commands should be quoted)
  -o --hour=HOUR                 Changes hour to HOUR (in 24h format)
  -m --minute=MINUTE             Changes minute to MINUTE
  -d --disable                   Disables task
  -e --enable                    Enables task
  -t --toggle                    Toggles enable/disable state
  -q --quiet                     Turns off snake messages
  -p --porcelain                 Prints message in easy-to-parse format

Example: #todo:

"""
import logging
import sys

from docopt import docopt
from schema import And, Or, Schema, Use

from pythonanywhere.scripts_commons import get_logger, validate_user_input
from pythonanywhere.snakesay import snakesay
from pythonanywhere.task import Task

logger = get_logger()


def main(**kwargs):
    def parse_opts(*opts):
        candidates = [key for key in opts if kwargs.pop(key)]
        return candidates[0] if candidates else None

    if not parse_opts("quiet"):
        logger.setLevel(logging.INFO)

    task_id = parse_opts("task_id")
    porcelain = parse_opts("porcelain")
    enable_opt = parse_opts("toggle", "disable", "enable")

    task = Task.from_id(task_id)

    params = {key: val for key, val in kwargs.items() if val}
    if enable_opt:
        enable_opt = {"toggle": not task.enabled, "disable": False, "enable": True}[enable_opt]
        params.update({"enabled": enable_opt})

    try:
        task.update_schedule(params, porcelain)
    except Exception as e:
        logger.warning(snakesay(str(e)))


if __name__ == "__main__":
    schema = ScriptSchema(
        {
            "<id>": Schemata.id_required,
            "--command": Schemata.string,
            "--hour": Schemata.hour,
            "--minute": Schemata.minute,
            "--disable": Schemata.boolean,
            "--enable": Schemata.boolean,
            "--toggle": Schemata.boolean,
            "--quiet": Schemata.boolean,
            "--porcelain": Schemata.boolean,
        }
    )
    arguments = schema.validate_user_input(docopt(__doc__))

    main(**arguments)

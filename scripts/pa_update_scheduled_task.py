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

from pythonanywhere.scripts_commons import validate_user_input
from pythonanywhere.snakesay import snakesay
from pythonanywhere.task import Task
from schema import And, Or, Schema, Use

logging.basicConfig(format="%(message)s", stream=sys.stdout)
logger = logging.getLogger(name=__name__)


def main(task_id, **kwargs):
    def parse_opts(*opts):
        candidates = [key for key in opts if kwargs.pop(key)]
        return candidates[0] if candidates else None

    logging_level = parse_opts("quiet", "porcelain")
    if logging_level != "quiet":
        logging.basicConfig(level=logging.INFO)

    enable_opt = parse_opts("toggle", "disable", "enable")

    task = Task.from_id(task_id)

    params = {key: val for key, val in kwargs.items() if val}
    if enable_opt:
        enable_opt = {"toggle": not task.enabled, "disable": False, "enable": True}[enable_opt]
        params.update({"enabled": enable_opt})

    try:
        task.update_schedule(params, logging_level=logging_level)
    except Exception as e:
        logger.warning(snakesay(str(e)))


if __name__ == "__main__":
    Boolean = Or(None, bool)
    Hour = Or(None, And(Use(int), lambda h: 0 <= h <= 23), error="--hour has to be in 0..23")
    Minute = Or(None, And(Use(int), lambda m: 0 <= m <= 59), error="--minute has to be in 0..59")
    schema = Schema(
        {
            "<id>": And(Use(int), error="<id> has to be an integer"),
            "--command": Or(None, str),
            "--hour": Hour,
            "--minute": Minute,
            "--disable": Boolean,
            "--enable": Boolean,
            "--toggle": Boolean,
            "--quiet": Boolean,
            "--porcelain": Boolean,
        }
    )
    arguments = validate_user_input(docopt(__doc__), schema)

    main(
        arguments["<id>"],
        command=arguments["--command"],
        hour=arguments["--hour"],
        minute=arguments["--minute"],
        disable=arguments["--disable"],
        enable=arguments["--enable"],
        toggle=arguments["--toggle"],
        quiet=arguments["--quiet"],
        porcelain=arguments["--porcelain"],
    )

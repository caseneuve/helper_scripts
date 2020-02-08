#!/usr/bin/python3.5
"""Update a scheduled task. Note that logfile name will change after updating the task
but it won't be created until first execution of the task.

Usage:
  pa_update_scheduled_task.py <id> [--command=CMD] [--hour=HOUR] [--minute=MINUTE]
                                   [--disable | --enable | --toggle-enabled]
                                   [--daily | --hourly]
                                   [--quiet | --porcelain]

Options:
  -h --help                      Print this message
  -c --command=CMD               Changes command to CMD (multiword commands should be quoted)
  -o --hour=HOUR                 Changes hour to HOUR (in 24h format)
  -m --minute=MINUTE             Changes minute to MINUTE
  -d --disable                   Disables task
  -e --enable                    Enables task
  -t --toggle-enabled            Toggles enable/disable state
  -a --daily                     Switches interval to daily (requires setting --hour,
                                 otherwise script's execution hour will be set)
  -u --hourly                    Switches interval to hourly (takes precedence over --hour
                                 meaning that hour will be set to None)
  -q --quiet                     Turns off snake messages
  -p --porcelain                 Prints message in easy-to-parse format

Example: #todo:

"""
import logging
from datetime import datetime

from docopt import docopt

from pythonanywhere.scripts_commons import ScriptSchema, get_logger, get_task_from_id
from pythonanywhere.snakesay import snakesay


def main(*, task_id, **kwargs):
    logger = get_logger()

    if kwargs.pop("hourly", False):
        kwargs["interval"] = "hourly"
    if kwargs.pop("daily", False):
        kwargs["hour"] = kwargs["hour"] if kwargs["hour"] else datetime.now().hour
        kwargs["interval"] = "daily"

    def parse_opts(*opts):
        candidates = [key for key in opts if kwargs.pop(key, None)]
        return candidates[0] if candidates else None

    if not parse_opts("quiet"):
        logger.setLevel(logging.INFO)

    porcelain = parse_opts("porcelain")
    enable_opt = parse_opts("toggle_enabled", "disable", "enable")

    task = get_task_from_id(task_id)

    params = {key: val for key, val in kwargs.items() if val}
    if enable_opt:
        enabled = {"toggle_enabled": not task.enabled, "disable": False, "enable": True}[
            enable_opt
        ]
        params.update({"enabled": enabled})

    try:
        task.update_schedule(params, porcelain=porcelain)
    except Exception as e:
        logger.warning(snakesay(str(e)))


if __name__ == "__main__":
    schema = ScriptSchema(
        {
            "<id>": ScriptSchema.id_required,
            "--command": ScriptSchema.string,
            "--daily": ScriptSchema.boolean,
            "--disable": ScriptSchema.boolean,
            "--enable": ScriptSchema.boolean,
            "--hour": ScriptSchema.hour,
            "--hourly": ScriptSchema.boolean,
            "--minute": ScriptSchema.minute,
            "--porcelain": ScriptSchema.boolean,
            "--quiet": ScriptSchema.boolean,
            "--toggle-enabled": ScriptSchema.boolean,
        }
    )
    arguments = schema.validate_user_input(docopt(__doc__))

    main(**arguments)

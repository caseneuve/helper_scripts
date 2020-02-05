#!/usr/bin/python3.5
"""Get current scheduled task's specs file by task id.
Available specs are: command, enabled, interval, hour, minute.
If no option specified, script will output all mentioned specs.

Usage:
  pa_get_scheduled_task_specs.py <id> [--command] [--enabled] [--interval] [--hour] [--minute] [--printable-time] [--snakesay]

Options:
  -h --help                      Prints this message
  -c --command                   Prints task's command
  -e --enabled                   Prints True if task is enabled 
  -i --interval                  Prints task's frequency (daily or hourly)
  -o --hour                      Prints task's scheduled hour (if daily)
  -m --minute                    Prints task's scheduled minute
  -s --snakesay                  Turns on snakesay... because why not

Note:
  Task <id> may be found using pa_get_scheduled_tasks_list.py script.
"""

import logging

from docopt import docopt
from schema import And, Schema, Use
from tabulate import tabulate

from pythonanywhere.scripts_commons import validate_user_input
from pythonanywhere.snakesay import snakesay
from pythonanywhere.task import Task

logger = logging.getLogger(name=__name__)
logger.setLevel(logging.INFO)


def main(task_id, **kwargs):
    try:
        task = Task.from_id(task_id)
    except Exception as e:
        print(snakesay("Ooops. {e}".format(e=e)))

    snake = kwargs.pop("snake")

    specs = (
        {spec: getattr(task, spec) for spec in kwargs if kwargs[spec]}
        if any([val for val in kwargs.values()])
        else {spec: getattr(task, spec) for spec in kwargs}
    )

    # get user path instead of server path:
    if kwargs["logfile"]:
        specs.update({"logfile": task.logfile.replace("/user/{}".format(task.username), "")})

    intro = "Task {} specs: ".format(task_id)
    if snake:
        specs = ["<{}>: {}".format(spec, value) for spec, value in specs.items()]
        specs.sort()
        logger.info(snakesay(intro + ", ".join(specs)))
    else:
        table = [[spec, val] for spec, val in specs.items()]
        table.sort(key=lambda x: x[0])
        logger.info(intro)
        logger.info(tabulate(table, tablefmt="simple"))


if __name__ == "__main__":
    Boolean = Or(None, bool)
    schema = Schema(
        {
            "<id>": And(Use(int), error="<id> should be an integer"),
            "--command": Boolean,
            "--enabled": Boolean,
            "--hour": Boolean,
            "--interval": Boolean,
            "--logfile": Boolean,
            "--minute": Boolean,
            "--snakesay": Boolean,
        }
    )
    arguments = validate_user_input(docopt(__doc__), schema)

    main(
        int(arguments["<id>"]),
        command="--command",
        enabled=arguments["--enabled"],
        hour=arguments["--hour"],
        interval=arguments["--interval"],
        logfile=arguments["--logfile"],
        minute=arguments["--minute"],
        snake=arguments["--snakesay"],
    )

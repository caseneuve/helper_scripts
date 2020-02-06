#!/usr/bin/python3.5
"""Get current scheduled task's specs file by task id.
Available specs are: command, enabled, interval, hour, minute.
If no option specified, script will output all mentioned specs.

Usage:
  pa_get_scheduled_task_specs.py <id> [--command] [--enabled] [--interval] [--hour] [--minute] [--printable-time] [--logfile] [--expiry] [--snakesay | --values]

Options:
  -h --help                      Prints this message
  -c --command                   Prints task's command
  -e --enabled                   Prints True if task is enabled
  -i --interval                  Prints task's frequency (daily or hourly)
  -l --logfile                   Prints task's current log file name
  -m --minute                    Prints task's scheduled minute
  -o --hour                      Prints task's scheduled hour (if daily)
  -p --printable-time            Prints task's scheduled time
  -x --expiry                    Prints task's expiry date
  -v --values                    Prints only values without spec names
  -s --snakesay                  Turns on snakesay... because why not

Note:
  Task <id> may be found using pa_get_scheduled_tasks_list.py script.
"""

from docopt import docopt
from tabulate import tabulate

from pythonanywhere.scripts_commons import ScriptSchema, get_logger, get_task_from_id
from pythonanywhere.snakesay import snakesay


def main(**kwargs):
    logger = get_logger(set_info=True)

    task_id = kwargs.pop("task_id")
    task = get_task_from_id(task_id)

    print_snake = kwargs.pop("snake")
    print_only_values = kwargs.pop("values")

    specs = (
        {spec: getattr(task, spec) for spec in kwargs if kwargs[spec]}
        if any([val for val in kwargs.values()])
        else {spec: getattr(task, spec) for spec in kwargs}
    )

    # get user path instead of server path:
    if specs.get("logfile"):
        specs.update({"logfile": task.logfile.replace("/user/{}/files".format(task.user), "")})

    intro = "Task {} specs: ".format(task_id)
    if print_only_values:
        specs = "\n".join([str(val) for val in specs.values()])
        logger.info(specs)
    elif print_snake:
        specs = ["<{}>: {}".format(spec, value) for spec, value in specs.items()]
        specs.sort()
        logger.info(snakesay(intro + ", ".join(specs)))
    else:
        table = [[spec, val] for spec, val in specs.items()]
        table.sort(key=lambda x: x[0])
        logger.info(intro)
        logger.info(tabulate(table, tablefmt="simple"))


if __name__ == "__main__":
    schema = ScriptSchema(
        {
            "<id>": ScriptSchema.id_required,
            "--command": ScriptSchema.boolean,
            "--enabled": ScriptSchema.boolean,
            "--expiry": ScriptSchema.boolean,
            "--hour": ScriptSchema.boolean,
            "--interval": ScriptSchema.boolean,
            "--logfile": ScriptSchema.boolean,
            "--minute": ScriptSchema.boolean,
            "--printable-time": ScriptSchema.boolean,
            "--values": ScriptSchema.boolean,
            "--snakesay": ScriptSchema.boolean,
        }
    )
    arguments = schema.validate_user_input(docopt(__doc__))

    main(**arguments)

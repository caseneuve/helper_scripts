#!/usr/bin/python3.5
"""Delete scheduled task(s) by id.

Usage:
  pa_delete_scheduled_task.py ids <num>...
  pa_delete_scheduled_task.py nuke [--force]

Options:
  -h, --help                  Prints this message
  -f, --force                 Bla

Note:
  Task <id> may be found using `pa_get_scheduled_tasks_list.py` script."""

import sys

from docopt import docopt

from pythonanywhere.scripts_commons import ScriptSchema, get_logger, get_task_from_id
from pythonanywhere.task import TaskList


def main(*, ids, num, nuke, force):
    get_logger(set_info=True)

    if nuke:
        if not force:
            try:
                decision = input("This will irrevocably delete all your tasks, proceed? [y/N] ")
            except Exception:
                pass
            if decision.lower() != "y":
                sys.exit()
        tasks = [task.task_id for task in TaskList().tasks]
    else:
        tasks = num

    for task in tasks:
        try:
            task = get_task_from_id(task, no_exit=True)
            task.delete_schedule()
        except Exception:
            pass


if __name__ == "__main__":
    schema = ScriptSchema(
        {
            "ids": bool,
            "<num>": ScriptSchema.id_multi,
            "nuke": bool,
            "--force": ScriptSchema.boolean,
        }
    )
    main(**schema.validate_user_input(docopt(__doc__)))

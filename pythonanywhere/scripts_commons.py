import logging
import sys

from schema import And, Or, Schema, SchemaError, Use

from pythonanywhere.snakesay import snakesay
from pythonanywhere.task import Task

logger = logging.getLogger(__name__)

tabulate_formats = [
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


class ScriptSchema(Schema):
    boolean = Or(None, bool)
    hour = Or(None, And(Use(int), lambda h: 0 <= h <= 23), error="--hour has to be in 0..23")
    minute_required = And(Use(int), lambda m: 0 <= m <= 59, error="--minute has to be in 0..59")
    minute = Or(None, minute_required)
    id_required = And(Use(int), error="<id> has to be an integer")
    string = Or(None, str)
    tabulate_format = Or(
        None,
        And(str, lambda f: f in tabulate_formats),
        error="--format should match one of: {}".format(", ".join(tabulate_formats)),
    )

    def init(self, schema):
        super().__init__(schema=schema)

    def convert(self, string):
        to_be_replaced = {
            "--": "",
            "<": "",
            ">": "",
            "printable-": "printable_",
            "snakesay": "snake",
            "id": "task_id",
        }
        for key, value in to_be_replaced.items():
            string = string.replace(key, value)
        return string

    def validate_user_input(self, arguments):
        try:
            self.validate(arguments)
            return {self.convert(key): val for key, val in arguments.items()}
        except SchemaError as e:
            logger.warning(snakesay(str(e)))
            sys.exit(1)


def get_logger(set_info=False):
    logging.basicConfig(format="%(message)s", stream=sys.stdout)
    logger = logging.getLogger("pythonanywhere")
    if set_info:
        logger.setLevel(logging.INFO)
    return logger


def get_task_from_id(task_id):
    try:
        return Task.from_id(task_id)
    except Exception as e:
        logger.warning(snakesay(str(e)))
        sys.exit(1)

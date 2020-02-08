"""Helpers used by pythonanywhere helper scripts."""

import logging
import sys

from schema import And, Or, Schema, SchemaError, Use

from pythonanywhere.snakesay import snakesay
from pythonanywhere.task import Task

logger = logging.getLogger(__name__)

# fmt: off
tabulate_formats = [
    "plain", "simple", "github", "grid", "fancy_grid", "pipe", "orgtbl", "jira",
    "presto", "psql", "rst", "mediawiki", "moinmoin", "youtrack", "html", "latex",
    "latex_raw", "latex_booktabs", "textile",
]
# fmt: on


class ScriptSchema(Schema):
    """Extends `Schema` adapting it to PA scripts validation strategies.

    Adds predefined schemata as class variables to be used in scripts'
    validation schemas as well as `validate_user_input` method wich acts
    as `Schema.validate` but returns a dictionary with converted keys
    ready to be used as function keyword arguments, e.g. validated
    arguments {"--foo": bar, "<baz>": qux} will be be converted to
    {"foo": bar, "baz": qux}.

    Use :method:`ScriptSchema.validate_user_input` to obtain kwarg
    dictionary."""

    # class variables are used in task scripts schemata:
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

    @staticmethod
    def convert(string):
        """Removes cli arguement notation characters ('--', '<', '>' etc.).

        :param string: cli argument key to be converted to fit Python
        argument syntax."""

        to_be_replaced = {
            "--": "",
            "<": "",
            ">": "",
            # below are hardcoded cases used in task scripts; todo: extract this separate argument
            # to make it more explicit in scripts and enable universal usage of adding any
            # replacement combinations
            "id": "task_id",
            "no-": "no_",
            "printable-": "printable_",
            "snakesay": "snake",
            "toggle-": "toggle_",
        }
        for key, value in to_be_replaced.items():
            string = string.replace(key, value)
        return string

    def validate_user_input(self, arguments):
        """Calls `Schema.validate` on provided `arguments`.

        Returns dictionary with keys converted by
        `ScriptSchema.convert` :method: to be later used as kwarg
        arguements.

        :param arguments: dictionary of cli arguments provided be
        (e.g.) `docopt`"""

        try:
            self.validate(arguments)
            return {self.convert(key): val for key, val in arguments.items()}
        except SchemaError as e:
            logger.warning(snakesay(str(e)))
            sys.exit(1)


def get_logger(set_info=False):
    """Sets logger for 'pythonanywhere' package.

    Returns `logging.Logger` instance with no message formatting which
    will stream to stdout. With `set_info` :param: set to `True`
    logger defines `logging.INFO` level otherwise it leaves default
    `logging.WARNING`.

    To toggle message visibility in scripts use `logger.info` calls
    and switch `set_info` value accordingly.

    *Note*: function should be called inside scripts' functions
    to prevent setting logger during module imports.

    :param set_info: boolean (defaults to False)"""

    logging.basicConfig(format="%(message)s", stream=sys.stdout)
    logger = logging.getLogger("pythonanywhere")
    if set_info:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)
    return logger


def get_task_from_id(task_id):
    """Get `Task.from_id` instance representing existing task.

    :param task_id: integer (should be a valid task id)"""

    try:
        return Task.from_id(task_id)
    except Exception as e:
        logger.warning(snakesay(str(e)))
        sys.exit(1)

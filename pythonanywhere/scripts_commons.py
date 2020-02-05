import logging
import sys

from schema import SchemaError, Schema, Or, And, Use


class Schemata:
    boolean = Or(None, bool)
    hour = Or(None, And(Use(int), lambda h: 0 <= h <= 23), error="--hour has to be in 0..23")
    minute = Or(None, And(Use(int), lambda m: 0 <= m <= 59), error="--minute has to be in 0..59")
    minute_required = And(Use(int), lambda m: 0 <= m <= 59, error="--minute has to be in 0..59")
    id_required = And(Use(int), error="<id> has to be an integer")
    string = Or(None, str)


class ScriptSchema(Schema):
    def init(self, schema):
        super().__init__(schema=schema)

    def convert(self, string):
        to_be_replaced = {"id": "task_id", "snakesay": "snake", "--": "", "<": "", ">": ""}
        for k, v in to_be_replaced.items():
            string = string.replace(k, v)
        return string

    def validate_user_input(self, arguments):
        try:
            self.validate(arguments)
            return {self.convert(key): val for key, val in arguments.items()}
        except SchemaError as e:
            print(e)
            sys.exit(1)


def validate_user_input(arguments, schema):
    try:
        return schema.validate(arguments)
    except SchemaError as e:
        print(e)
        sys.exit(1)


def get_logger(set_info=False):
    logging.basicConfig(format="%(message)s", stream=sys.stdout)
    logger = logging.getLogger("pythonanywhere")
    if set_info:
        logger.setLevel(logging.INFO)
    return logger

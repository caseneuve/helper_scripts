import sys

from schema import SchemaError


def validate_user_input(arguments, schema):
    try:
        return schema.validate(arguments)
    except SchemaError as e:
        print(e)
        sys.exit(1)

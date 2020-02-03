from unittest.mock import call

import pytest
from schema import And, Schema, SchemaError
from scripts.script_commons import validate_user_input

example_schema = Schema(
    {
        "a": And(int, lambda a: a > 0, error="<a> should be bigger than 0"),
        "b": And(
            str, lambda b: b.startswith("foo"), error="<b> should start with 'foo'"
        ),
    }
)


class TestValidateUserInput:
    def test_returns_arguments(self):
        args = {"a": 1, "b": "foobar"}

        result = validate_user_input(args, example_schema)

        assert result == args

    def test_raises_because_arguments_dont_match_schema(self, mocker):
        args = {"a": 0, "b": "foobaz"}
        mock_print = mocker.patch("builtins.print")
        mock_exit = mocker.patch("scripts.script_commons.sys.exit")

        validate_user_input(args, example_schema)

        assert mock_exit.call_args == call(1)
        assert (
            repr(mock_print.call_args[0])
            == "(SchemaError('<a> should be bigger than 0',),)"
        )

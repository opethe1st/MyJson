import json

import pytest

import myjson
import os


@pytest.mark.parametrize(
    ("description", "string"),
    [
        ('test that this works for a simple mapping', '{"key": "value"}', ),
        ('test that this works for a mapping that has a value that is a mapping', '{"key": {"key": "value"}}'),
        ('test that this works for a sequence of scalars', '["key", "value"]'),
        ('test that this works for a sequence of mappings', '[{"key": "value"}, {"key2": "value"}]'),
        ('test that this works for a string', '"value"'),
        ('test that this works for a realistic json ', '"value"'),
        ('test that this works for a realistic json ', '1234'), # added deliberately failing test to see if ci catches it
    ]
)
def test_loading(description, string):
    assert myjson.loads(string) == json.loads(string)


@pytest.mark.parametrize(
    ("description", "filename"),
    [
        ('test that this works for a realistic json ', 'sample.json'),
    ]
)
def test_loading_from_file(description, filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    with open(filename) as f:
        string = f.read()
        assert myjson.loads(string) == json.loads(string)

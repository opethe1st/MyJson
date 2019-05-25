import json

import pytest

import myjson


@pytest.mark.xfail
@pytest.mark.parametrize(
    ("description", "string"),
    [
        ('test that this works for a simple mapping', '{"key": "value"}', ),
        ('test that this works for a mapping that has a value that is a mapping', '{"key": {"key": "value"}}', ),
        ('test that this works for a sequence of scalars', '["key", "value"]', ),
        ('test that this works for a sequence of mappings', '[{"key": "value"}, {"key2": "value"}]', ),
        ('test that this works for a string', '"value"', ),
    ]
)
def test_loading(description, string):
    assert myjson.loads(string) == json.loads(string)

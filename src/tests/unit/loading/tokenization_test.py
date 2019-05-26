from unittest import TestCase

from myjson.loading.tokenization import (
    Delimiter,
    MappingEnd,
    MappingStart,
    ScalarValue,
    Separator,
    SequenceEnd,
    SequenceStart,
    tokenize
)


class TestTokenize(TestCase):

    # this could be parametrized since it is testing a function
    def test_1(self):
        '''Test that string get converted to expected token'''
        self.assertEqual(
            tokenize(string='"string"'),
            [ScalarValue(data='string')]
        )

    def test_2(self):
        '''Test that mapping get converted to expected token'''
        self.assertEqual(
            tokenize(string='{"key": "value", "key2":"value"}'),
            [
                MappingStart(),
                ScalarValue(data='key'),
                Separator(),
                ScalarValue(data='value'),
                Delimiter(),
                ScalarValue(data='key2'),
                Separator(),
                ScalarValue(data='value'),
                MappingEnd()
            ]
        )

    def test_3(self):
        '''Test that a sequence is converted to the expected token'''
        self.assertEqual(
            tokenize(string='["key", "value", "key2","value"]'),
            [
                SequenceStart(),
                ScalarValue(data='key'),
                Delimiter(),
                ScalarValue(data='value'),
                Delimiter(),
                ScalarValue(data='key2'),
                Delimiter(),
                ScalarValue(data='value'),
                SequenceEnd()
            ]
        )

    def test_4(self):
        '''Test that a string is converted to its expected tokens when it spans more than one line'''
        self.assertEqual(
            tokenize(string='''[
                "key",
                "value",
                "key2",
                "value"
                ]'''
            ),
            [
                SequenceStart(),
                ScalarValue(data='key'),
                Delimiter(),
                ScalarValue(data='value'),
                Delimiter(),
                ScalarValue(data='key2'),
                Delimiter(),
                ScalarValue(data='value'),
                SequenceEnd()
            ]
        )

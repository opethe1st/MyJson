from unittest import TestCase

from myjson.core import MappingNode, ScalarNode, SequenceNode
from myjson.loading.node_from_tokens import (
    is_mapping,
    is_scalar,
    is_sequence,
    mapping_node_from_tokens,
    scalar_node_from_tokens,
    sequence_node_from_tokens
)
from myjson.loading.tokenization import (
    MappingEnd,
    MappingStart,
    ScalarValue,
    Separator,
    SequenceEnd,
    SequenceStart,
    Delimiter,
)


class TestIsMapping(TestCase):

    def test_1(self):
        '''Test that is_mapping is true if we check from the first token in this {"key": "value"} '''
        self.assertTrue(
            is_mapping(tokens=[
                MappingStart(),
                ScalarValue(data='key'),
                Separator(),
                ScalarValue(data='value'),
                MappingEnd(),
            ], start=0)
        )

    def test_2(self):
        '''Test that is_mapping is false if we check from the second token in this "key": "value"} '''
        self.assertFalse(
            is_mapping(tokens=[
                MappingStart(),
                ScalarValue(data='key'),
                Separator(),
                ScalarValue(data='value'),
                MappingEnd(),
            ], start=1)
        )


class TestIsSequence(TestCase):

    def test_is_sequence(self):
        self.assertTrue(
            is_sequence(tokens=[
                SequenceStart(),
                ScalarValue(data='value'),
                SequenceEnd(),
            ], start=0)
        )


class TestIsScalar(TestCase):

    def test_is_scalar(self):
        self.assertTrue(
            is_scalar(tokens=[ScalarValue(data='value')], start=0)
        )



class TestScalarNodeFromTokens(TestCase):

    def test_scalar_node_from_tokens(self):
        self.assertEqual(
            scalar_node_from_tokens(tokens=[ScalarValue(data='value')], start=0),
            (ScalarNode(data='value'), 1),
        )


class TestSequenceNodeFromTokens(TestCase):

    def test_1(self):
        '''test that sequence_node_from_tokens works for the simplest case'''
        self.assertEqual(
            sequence_node_from_tokens(tokens=[
                SequenceStart(),
                ScalarValue(data='value'),
                SequenceEnd(),
            ], start=0),
            (SequenceNode(items=[ScalarNode(data='value')]), 3)
        )

    def test_2(self):
        '''test that sequence_node_from_tokens works when there is no item'''
        self.assertEqual(
            sequence_node_from_tokens(tokens=[
                SequenceStart(),
                SequenceEnd(),
            ], start=0),
            (SequenceNode(items=[]), 2)
        )

    def test_3(self):
        '''test that sequence_node_from_tokens works with more than one item'''
        self.assertEqual(
            sequence_node_from_tokens(tokens=[
                SequenceStart(),
                ScalarValue(data='value'),
                Delimiter(),
                ScalarValue(data='value'),
                SequenceEnd(),
            ], start=0),
            (SequenceNode(items=[ScalarNode(data='value'), ScalarNode(data='value')]), 5)
        )

    def test_4(self):
        '''test that sequence_node_from_tokens works with there is a nested sequence'''
        self.assertEqual(
            sequence_node_from_tokens(tokens=[
                SequenceStart(),
                SequenceStart(),
                ScalarValue(data='value'),
                SequenceEnd(),
                SequenceEnd(),
            ], start=0),
            (SequenceNode(items=[SequenceNode(items=[ScalarNode(data='value')])]), 5)
        )

    def test_5(self):
        '''test that sequence_node_from_tokens works with it contains a mapping'''
        self.assertEqual(
            sequence_node_from_tokens(tokens=[
                SequenceStart(),
                MappingStart(),
                ScalarValue(data='key'),
                Separator(),
                ScalarValue(data='value'),
                MappingEnd(),
                SequenceEnd(),
            ], start=0),
            (SequenceNode(items=[MappingNode(mapping={ScalarNode(data='key'): ScalarNode(data='value')})]), 7)
        )


class TestMappingNodeFromTokens(TestCase):

    def test_1(self):
        '''test that mapping_node_from_tokens works for the simplest case'''
        self.assertEqual(
            mapping_node_from_tokens(tokens=[
                MappingStart(),
                ScalarValue(data='key'),
                Separator(),
                ScalarValue(data='value'),
                MappingEnd(),
            ], start=0),
            (MappingNode(mapping={ScalarNode(data='key'): ScalarNode(data='value')}), 5)
        )

    def test_2(self):
        '''test that mapping_node_from_tokens works when there are two items'''
        self.assertEqual(
            mapping_node_from_tokens(tokens=[
                MappingStart(),
                ScalarValue(data='key'),
                Separator(),
                ScalarValue(data='value'),
                Delimiter(),
                ScalarValue(data='key1'),
                Separator(),
                ScalarValue(data='value'),
                MappingEnd(),
            ], start=0),
            (MappingNode(mapping={
                ScalarNode(data='key'): ScalarNode(data='value'),
                ScalarNode(data='key1'): ScalarNode(data='value'),
                }),
            9)
        )

    def test_3(self):
        '''test that mapping_node_from_tokens works when there is a nested mapping'''
        self.assertEqual(
            mapping_node_from_tokens(tokens=[
                MappingStart(),
                ScalarValue(data='key'),
                Separator(),
                MappingStart(),
                ScalarValue(data='key1'),
                Separator(),
                ScalarValue(data='value'),
                MappingEnd(),
                MappingEnd(),
            ], start=0),
            (MappingNode(mapping={
                ScalarNode(data='key'): MappingNode(mapping={
                    ScalarNode(data='key1'): ScalarNode(data='value')
                    }),
                }),
            9)
        )

    def test_4(self):
        '''test that mapping_node_from_tokens works when the value is a sequence'''
        self.assertEqual(
            mapping_node_from_tokens(tokens=[
                MappingStart(),
                ScalarValue(data='key'),
                Separator(),
                SequenceStart(),
                ScalarValue(data='value'),
                SequenceEnd(),
                MappingEnd(),
            ], start=0),
            (MappingNode(mapping={
                ScalarNode(data='key'): SequenceNode(items=[ScalarNode(data='value')]),
            }),
            7)
        )

    def test_5(self):
        '''test that mapping_node_from_tokens works for when the mapping is empty'''
        self.assertEqual(
            mapping_node_from_tokens(tokens=[
                MappingStart(),
                MappingEnd(),
            ], start=0),
            (MappingNode(mapping={}), 2)
        )

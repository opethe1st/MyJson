from enum import Enum
from typing import List, Tuple

from myjson.core import MappingNode, Node, ScalarNode, SequenceNode

from .tokenization import (
    Delimiter,
    MappingEnd,
    MappingStart,
    ScalarValue,
    Separator,
    SequenceEnd,
    SequenceStart,
    Token,
    tokenize
)


def node_from_tokens(tokens: List['Token'], start: int) -> Tuple['Node', int]:
    if is_mapping(tokens=tokens, start=start):
        return mapping_node_from_tokens(tokens=tokens, start=start)
    elif is_sequence(tokens=tokens, start=start):
        return sequence_node_from_tokens(tokens=tokens, start=start)
    elif is_scalar(tokens=tokens, start=start):
        return scalar_node_from_tokens(tokens=tokens, start=start)
    raise Exception('Unrecognized tokens')


def is_mapping(tokens: List['Token'], start: int) -> bool:
    if start < len(tokens):
        return isinstance(tokens[start], MappingStart)
    else:
        return False


def mapping_node_from_tokens(tokens: List['Token'], start: int) -> Tuple['MappingNode', int]:
    mapping = {}
    currentPosition = start + 1
    while not isinstance(tokens[currentPosition], MappingEnd): # what happens if there is no end?
        keyNode, lastPosition = scalar_node_from_tokens(tokens=tokens, start=currentPosition)
        if not isinstance(tokens[lastPosition], Separator):
            raise Exception('Expected separator here')
        valueNode, lastPosition = node_from_tokens(tokens=tokens, start=lastPosition+1) # + 1 because it has consumed the separator
        mapping[keyNode] = valueNode
        if isinstance(tokens[lastPosition], Delimiter):
            lastPosition += 1
        currentPosition = lastPosition
    return MappingNode(mapping=mapping), currentPosition + 1


def is_sequence(tokens: List['Token'], start: int) -> bool:
    if start < len(tokens):
        return isinstance(tokens[start], SequenceStart)
    else:
        return False


def sequence_node_from_tokens(tokens: List['Token'], start: int) -> Tuple['SequenceNode', int]:
    items = []
    currentPosition = start + 1
    while not isinstance(tokens[currentPosition], SequenceEnd): # what happens if there is no end?
        valueNode, lastPosition = node_from_tokens(tokens=tokens, start=currentPosition) # it has consumed the separator
        items.append(valueNode)
        if isinstance(tokens[lastPosition], Delimiter):
            lastPosition += 1
        currentPosition = lastPosition
    return SequenceNode(items=items), currentPosition + 1


def is_scalar(tokens: List['Token'], start: int) -> bool:
    if start < len(tokens):
        return isinstance(tokens[start], ScalarValue)
    else:
        return False


def scalar_node_from_tokens(tokens: List['Token'], start: int) -> Tuple['ScalarNode', int]:
    if start >= len(tokens):
        raise Exception('start is pass the number of tokens')
    if not isinstance(tokens[start], ScalarValue):
        raise Exception('Trying to get a scalar node from a non-scalar node')
    return ScalarNode(data=tokens[start].data), start+1  # type: ignore

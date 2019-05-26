from myjson.core import Node

from .node_from_tokens import node_from_tokens
from .object_from_node import object_from_node
from .tokenization import tokenize


def loads(string: str) -> 'Node':
    tokens = tokenize(string=string)
    node, _ = node_from_tokens(tokens=tokens, start=0)
    return object_from_node(node)

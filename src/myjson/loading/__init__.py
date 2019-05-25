from .tokenization import (
    tokenize
)
from .node_from_tokens import node_from_tokens
from .object_from_node import object_from_node


def loads(string):
    tokens = tokenize(string=string)
    node = node_from_tokens(tokens=tokens, start=0)
    return object_from_node(node=node)

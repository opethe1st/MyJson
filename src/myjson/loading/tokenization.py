from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple

from .tokens import (
    Delimiter,
    MappingEnd,
    MappingStart,
    ScalarValue,
    Separator,
    SequenceEnd,
    SequenceStart,
    Token
)


def tokenize(string: str) -> List['Token']:
    tokens: List['Token'] = []
    currentState: 'State' = Unquoted()
    allTokens: List['Token'] = []
    for letter in string:
        currentState, tokens = currentState.transition(inp=letter)
        allTokens.extend(tokens)
    return allTokens


class State(ABC):
    @abstractmethod
    def transition(self, inp: str) -> Tuple['State', List['Token']]:
        pass


@dataclass
class Unquoted(State):

    def transition(self, inp: str) -> Tuple['State', List['Token']]:
        if inp == '{':
            return self, [MappingStart()]
        elif inp == '}':
            return self, [MappingEnd()]
        elif inp == '[':
            return self, [SequenceStart()]
        elif inp == ']':
            return self, [SequenceEnd()]
        elif inp == ':':
            return self, [Separator()]
        elif inp == ',':
            return self, [Delimiter()]
        elif inp in {' ', '\n'}:
            return self, []
        elif inp == '"':
            return Quoted(), []
        raise Exception('unknown special character')


@dataclass
class Quoted(State):
    data: str = ''
    def transition(self, inp: str) -> Tuple['State', List['Token']]:
        if inp == '"':
            return Unquoted(), [ScalarValue(data=self.data)]
        else:
            self.data += inp
            return self, []

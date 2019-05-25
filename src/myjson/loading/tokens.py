from dataclasses import dataclass


@dataclass
class Token:
    pass


@dataclass
class MappingStart(Token):
    pass


@dataclass
class MappingEnd(Token):
    pass


@dataclass
class Delimiter(Token):
    pass


@dataclass
class SequenceStart(Token):
    pass


@dataclass
class SequenceEnd(Token):
    pass


@dataclass
class ScalarValue(Token):
    data: str


@dataclass
class Separator(Token):
    pass

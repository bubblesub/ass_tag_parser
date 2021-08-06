from typing import Optional


class BaseError(Exception):
    pass


class ParseError(BaseError):
    def __init__(self, pos: int, msg: Optional[str] = None) -> None:
        text = f"syntax error at pos {pos}"
        if msg:
            text += f": {msg}"
        super().__init__(text)


class UnexpectedCurlyBrace(ParseError):
    def __init__(self, pos: int) -> None:
        super().__init__(pos, "unexpected curly brace")


class UnknownTag(ParseError):
    def __init__(self, pos: int) -> None:
        super().__init__(pos, "unrecognized tag")


class UnterminatedCurlyBrace(ParseError):
    def __init__(self, pos: int) -> None:
        super().__init__(pos, "unterminated curly brace")


class BadAssTagArgument(ParseError):
    def __init__(self, pos: int, msg: Optional[str] = None) -> None:
        super().__init__(pos, "bad ass argument" if msg is None else msg)

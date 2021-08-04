import io
from typing import Optional


class MyIO:
    def __init__(
        self,
        text: str = "",
        parent_pos: int = 0,
        global_text: Optional[str] = None,
    ) -> None:
        self._io = io.StringIO(text)
        self._text = text
        self._global_text = global_text or text
        self._size = len(text)
        self._parent_pos = parent_pos

    @property
    def eof(self) -> bool:
        return self.pos == self._size

    @property
    def pos(self) -> int:
        return self._io.tell()

    @property
    def global_pos(self) -> int:
        return self._parent_pos + self.pos

    @property
    def global_text(self) -> str:
        return self._global_text

    @property
    def text(self) -> str:
        pos = self._io.tell()
        self._io.seek(0)
        ret = self._io.read()
        self._io.seek(pos)
        return ret

    def read(self, num: int) -> str:
        return self._io.read(num)

    def write(self, text: str) -> None:
        self._io.write(text)

    def skip(self, num: int) -> None:
        self._io.seek(self.pos + num)

    def peek(self, num: int) -> str:
        old_pos = self._io.tell()
        ret = self._io.read(num)
        self._io.seek(old_pos)
        return ret

    def divide(self, start: int, end: int) -> "MyIO":
        return MyIO(
            self._text[start:end], self._parent_pos + start, self._global_text
        )

from ..ass_tag_clip import AssTagClipRectangle, AssTagClipVector
from dataclasses import dataclass


@dataclass
class AssValidTagClipRectangle(AssTagClipRectangle):
    x1: int
    y1: int
    x2: int
    y2: int

    def __str__(self):
        return f"\\{self.tag}({self.x1},{self.y1},{self.x2},{self.y2})"


@dataclass
class AssValidTagClipVector(AssTagClipVector):
    """
    If you wanna parse an Vector Clip, see the PyonFX library.
    Especially the Shape module: https://pyonfx.readthedocs.io/en/latest/reference/shape.html
    """

    path: str
    scale: int = 1

    def __str__(self):
        if self.scale == 1:
            return f"\\{self.tag}({self.path})"
        return f"\\{self.tag}({self.scale},{self.path})"

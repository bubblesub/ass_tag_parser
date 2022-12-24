from ..ass_tag_wrap_style import AssTagWrapStyle, WrapStyle
from dataclasses import dataclass


@dataclass
class AssValidTagWrapStyle(AssTagWrapStyle):
    style: WrapStyle

    def __str__(self):
        return f"\\{self.tag}{self.style.value}"

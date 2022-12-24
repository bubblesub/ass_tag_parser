from ..ass_tag_karaoke import AssTagKaraoke, AssTagKaraokeFill, AssTagKaraokeOutline
from dataclasses import dataclass


@dataclass
class AssValidTagKaraoke(AssTagKaraoke):
    duration: float  # In ms

    def __str__(self):
        return f"\\{self.tag}{self.duration // 10}"


@dataclass
class AssValidTagKaraokeFill(AssTagKaraokeFill):
    duration: float  # In ms

    def __str__(self):
        if self.is_short_tag:
            return f"\\{self.short_tag}{self.duration // 10}"
        return f"\\{self.tag}{self.duration // 10}"


@dataclass
class AssValidTagKaraokeOutline(AssTagKaraokeOutline):
    duration: float  # In ms

    def __str__(self):
        return f"\\{self.tag}{self.duration // 10}"

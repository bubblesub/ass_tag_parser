from ..ass_tag_fade import AssTagFade, AssTagFadeComplex
from dataclasses import dataclass


@dataclass
class AssValidTagFade(AssTagFade):
    time1: int
    time2: int

    def __str__(self):
        return f"\\{self.tag}({self.time1},{self.time2})"


@dataclass
class AssValidTagFadeComplex(AssTagFadeComplex):
    alpha1: int
    alpha2: int
    alpha3: int
    time1: int
    time2: int
    time3: int
    time4: int

    def __str__(self):
        return f"\\{self.tag}({self.alpha1},{self.alpha2},{self.alpha3},{self.time1},{self.time2},{self.time3},{self.time4})"

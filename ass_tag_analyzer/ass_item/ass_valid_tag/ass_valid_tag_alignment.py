from ..ass_tag_alignment import AssTagAlignment, Alignment, LegacyAlignment
from dataclasses import dataclass
from typing import Union


@dataclass
class AssValidTagAlignment(AssTagAlignment):
    __alignment: Union[Alignment, LegacyAlignment]

    def __init__(
        self, alignment: Union[Alignment, LegacyAlignment], is_legacy_tag: bool = False
    ):
        self.is_legacy_tag = is_legacy_tag
        self.alignment = alignment

    def convert_to_a_tag(self):
        if not self.is_legacy_tag:
            self.is_legacy_tag = True
            self.alignment = LegacyAlignment[self.alignment.name]

    def convert_to_an_tag(self):
        if self.is_legacy_tag:
            self.is_legacy_tag = False
            self.alignment = Alignment[self.alignment.name]

    @property
    def alignment(self):
        return self.__alignment

    @alignment.setter
    def alignment(self, alignment: Union[Alignment, LegacyAlignment]):
        if self.is_legacy_tag:
            if isinstance(alignment, LegacyAlignment):
                self.__alignment = alignment
            else:
                raise ValueError("alignment need to be an LegacyAlignment instance")
        else:
            if isinstance(alignment, Alignment):
                self.__alignment = alignment
            else:
                raise ValueError("alignment need to be an Alignment instance")

    def __str__(self):
        if self.is_legacy_tag:
            return f"\\{self.legacy_tag}{self.alignment.value}"
        return f"\\{self.tag}{self.alignment.value}"

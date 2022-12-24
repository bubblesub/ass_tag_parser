from ..ass_item import AssTag
from dataclasses import dataclass


@dataclass
class AssInvalidTag(AssTag):
    """
    An AssInvalidTag is used when ass_tag_analyzer cannot know what is the value of an tag because it depend of the style of the line.
    Ex:
        "{\\i}Example" would return an AssInvalidTagItalic, because the text "Example" will totally depend on the style of the line.
        So, if the style is italic, then "Example" will be display in italic and vice-versa.

    Attributes:
        text (str): The text of an invalid tag. At 99% of the time, the text will be empty.
            Ex:
                "\\b99" would return AssInvalidTagBold("99") instanc which is a AssInvalidTag.
    """

    text: str

    def __str__(self):
        return f"\\{self.tag}{self.text}"

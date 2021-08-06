import re
from itertools import chain
from pathlib import Path
from typing import Iterable, Type

import pytest

from ass_tag_parser.ass_struct import AssItem
from ass_tag_parser.draw_struct import AssDrawCmd


def get_subclasses(cls: Type[object]) -> Iterable[Type[object]]:
    for subclass in cls.__subclasses__():
        yield from get_subclasses(subclass)
        yield subclass


@pytest.fixture(name="all_names")
def fixture_all_names(project_dir: Path) -> list[str]:
    path_to_init = project_dir / "__init__.py"
    assert path_to_init.exists()

    match = re.search(
        r"__all__ = (\[.+\])", path_to_init.read_text(), flags=re.DOTALL
    )
    assert match

    ret = eval(match.group(1))  # pylint: disable=eval-used
    assert isinstance(ret, list)
    return ret


@pytest.mark.parametrize(
    "cls", chain(get_subclasses(AssItem), get_subclasses(AssDrawCmd))
)
def test_module_exports(all_names: list[str], cls: Type[object]) -> None:
    """Test that ass_tag_parser.__init__.__all__ includes all defined ASS tags
    and draw commands.
    """
    assert cls.__name__ in all_names

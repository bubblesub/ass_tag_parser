import re
from pathlib import Path
from typing import Any, no_type_check

import black
import pytest


@no_type_check
def format_black(source: Any) -> str:
    return black.format_str(str(source), mode=black.Mode(line_length=79))


@pytest.fixture(name="readme_content")
def fixture_readme_content(repo_dir: Path) -> str:
    path_to_readme = repo_dir / "README.md"
    assert path_to_readme.exists()
    return path_to_readme.read_text()


@pytest.fixture(name="readme_code_snippet")
def fixture_readme_code_snippet(readme_content: str) -> str:
    match = re.search(r"```python3([^`]*)```", readme_content, flags=re.DOTALL)
    assert match
    return match.group(1).lstrip()


@pytest.fixture(name="readme_code_result")
def fixture_readme_code_result(readme_content: str) -> str:
    match = re.search(
        r"```python3 console([^`]*)```", readme_content, flags=re.DOTALL
    )
    assert match
    return match.group(1).lstrip()


def test_readme_code_up_to_date(
    capsys: Any, readme_code_snippet: str, readme_code_result: str
) -> None:
    """Test that the code example in the README.md matches the actual output
    from the library.
    """
    exec(readme_code_snippet)  # pylint: disable=exec-used
    actual_result = format_black(capsys.readouterr().out.strip())
    assert actual_result == readme_code_result


def test_readme_code_formatting(readme_code_snippet: str) -> None:
    """Test that the code example in the README.md is well-formatted."""
    assert readme_code_snippet == format_black(readme_code_snippet)

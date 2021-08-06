from pathlib import Path

import pytest


@pytest.fixture(name="project_dir")
def fixture_project_dir() -> Path:
    return Path(__file__).parent.parent


@pytest.fixture(name="repo_dir")
def fixture_repo_dir(project_dir: Path) -> Path:
    return project_dir.parent

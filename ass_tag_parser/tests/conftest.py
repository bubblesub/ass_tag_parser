from pathlib import Path

import pytest


@pytest.fixture
def project_dir() -> Path:
    return Path(__file__).parent.parent


@pytest.fixture
def repo_dir(project_dir: Path) -> Path:
    return project_dir.parent

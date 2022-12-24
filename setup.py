import os
import re
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = [\'\"](.+)[\'\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="ass_tag_analyzer",
    url="https://github.com/moi15moi/ass_tag_parser/",
    project_urls={
        "Source": "https://github.com/moi15moi/ass_tag_parser/",
        "Tracker": "https://github.com/moi15moi/ass_tag_parser/issues/",
    },
    author="moi15moi",
    author_email="moi15moismokerlolilol@gmail.com",
    description="Parse .ass tags.",
    long_description_content_type="text/markdown",
    version=find_version("ass_tag_analyzer", "__init__.py"),
    packages=["ass_tag_analyzer"],
    python_requires=">=3.8",
    extras_require={
        "dev": [
            "black",
            "pytest",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Other Audience",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    license="GNU LGPL 3.0 or later",
)

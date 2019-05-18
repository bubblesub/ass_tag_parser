from pathlib import Path

from setuptools import find_packages, setup

setup(
    author="rr-",
    author_email="rr-@sakuya.pl",
    name="ass_tag_parser",
    version="2.1.post0",
    description="Parser of ASS tags",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/rr-/ass_tag_parser",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
    ],
    packages=find_packages(),
    package_dir={"ass_tag_parser": "ass_tag_parser"},
    package_data={"ass_tag_parser": ["data/*.*"]},
    install_requires=["parsimonious"],
)

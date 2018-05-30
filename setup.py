from setuptools import setup, find_packages


setup(
    author='rr-',
    author_email='rr-@sakuya.pl',
    name='ass_tag_parser',
    version='0.4',
    long_description='Parser of ASS tags',
    packages=find_packages(),
    package_dir={'ass_tag_parser': 'ass_tag_parser'},
    package_data={'ass_tag_parser': ['data/*.*']},
    install_requires=['parsimonious'])

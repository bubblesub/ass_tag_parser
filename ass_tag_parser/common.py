import pathlib


DATA_DIR = pathlib.Path(__file__).parent / 'data'


class ParsingError(RuntimeError):
    pass


def flatten(items):
    if isinstance(items, (list, tuple)):
        return [
            item
            for sublist in items
            for item in flatten(sublist)
        ]
    return [items]

# AssTagAnalyzer
Tag analyzer for Advanced SubStation Alpha file.
This tool allows to parse .ass tag and manipulate them.

## Installation and Update
```
pip install ass-tag-analyzer
```

## Example
```py
from ass_tag_analyzer import parse_line, ass_item_to_text, Format, AssTagFontName, AssValidTagFontName, AssInvalidTagFontName

# Parse an .ass line
line = parse_line(r"{\an7\pos(158,501)\fnArial\bord0.155884}Example")
print(line)

# Convert line to text
print(ass_item_to_text(line))

# Change how to convert float to string
Format.format_float = lambda number: round(number)

# Reconvert line to text. See how the \bord result is different
print(ass_item_to_text(line))

# Search an tag
for ass_item in line:
    if isinstance(ass_item, AssTagFontName):
        if isinstance(ass_item, AssValidTagFontName):
            print(f'An \\fn tag has been found and the value is "{ass_item.name}"')

        elif isinstance(ass_item, AssInvalidTagFontName):
            # You need to get the style that is applied on the line.
            pass
```

### Result

```py console
[
    AssTagListOpening(),
    AssValidTagAlignment(is_legacy_tag=False, _AssValidTagAlignment__alignment=<Alignment.TOP_LEFT: 7>),
    AssValidTagPosition(x=158.0, y=501.0),
    AssValidTagFontName(_AssValidTagFontName__name='Arial'),
    AssValidTagBorder(_AssValidTagBorder__size=0.155884),
    AssTagListEnding(),
    AssText(text='Example')
]
{\an7\pos(158,501)\fnArial\bord0.156}Example
{\an7\pos(158,501)\fnArial\bord0}Example
An \fn tag has been found and the value is "Arial"
```

## Dependencies
-  [Python 3.8 or more](https://www.python.org/downloads/)


## Acknowledgments
 - [ass_tag_parser](https://github.com/bubblesub/ass_tag_parser) I used his library to create mine. I got a lot of inspiration from his work.

ass_tag_parser
==============

[![Actions Status](https://github.com/bubblesub/ass_tag_parser/workflows/ass_tag_parser/badge.svg)](https://github.com/bubblesub/ass_tag_parser/actions)

Library for parsing ASS tags.

Not to confuse with parsing `.ass` files that can be manipulated with
[`pysubs2`](https://github.com/tkarabela/pysubs2).


**Example**:

```python
from ass_tag_parser import parse_ass

result = parse_ass(
    r'{\an5\pos(175,460)\fnUtopia with Oldstyle figures\fs90\bord0\blur3'
    r'\1c&H131313&\t(0,1000,2,\1c&H131340&)\t(1000,2000,\1c&H1015B2&'
    r'\blur1.4)}Attack No. 1{NOTE:アタックNo.1}'
)
print(result)
print(result[2].meta)
```

**Result**:

```python3
[
    AssTagListOpening(),
    AssTagAlignment(alignment=5, legacy=False),
    AssTagPosition(x=175.0, y=460.0),
    AssTagFontName(name="Utopia with Oldstyle figures"),
    AssTagFontSize(size=90),
    AssTagBorder(size=0.0),
    AssTagBlurEdgesGauss(weight=3.0),
    AssTagColor(red=19, green=19, blue=19, target=1, short=False),
    AssTagAnimation(
        tags=[AssTagColor(red=64, green=19, blue=19, target=1, short=False)],
        time1=0.0,
        time2=1000.0,
        acceleration=2.0,
    ),
    AssTagAnimation(
        tags=[
            AssTagColor(red=178, green=21, blue=16, target=1, short=False),
            AssTagBlurEdgesGauss(weight=1.4),
        ],
        time1=1000.0,
        time2=2000.0,
        acceleration=None,
    ),
    AssTagListEnding(),
    AssText(text="Attack No. 1"),
    AssTagListOpening(),
    AssTagComment(text="NOTE:アタックNo.1"),
    AssTagListEnding(),
]


Meta(start=5, end=18, text='\\pos(175,460)')
```

Starting from version 2.2, drawing commands are parsed automatically.

---

### Serializing the tree back

ASS tree: `compose_ass`. Note that you don't need to supply `AssTagListOpening`
nor `AssTagListEnding` tags in the input item list – this function inserts them
automatically.

Draw commands: `compose_draw_commands`.

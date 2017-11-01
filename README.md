ass_tag_parser
==============

Library for parsing ASS tags.

Not to confuse with parsing `.ass` files that can be manipulated with
[`pysubs2`](https://github.com/tkarabela/pysubs2).


**Example**:

```python
from ass_tag_parser import parse_ass
import json

result = parse_ass(
    r'{\an5\pos(175,460)\fnUtopia with Oldstyle figures\fs90\bord0\blur3'
    r'\1c&H131313&\t(0,1000,2,\1c&H131340&)\t(1000,2000,\1c&H1015B2&'
    r'\blur1.4)}Attack No. 1{NOTE:アタックNo.1}')
print(json.dumps(result))
```

**Result**:

```json
[
    {
        "pos": [0, 138],
        "type": "tags",
        "children":
        [
            {"pos": [1, 5], "type": "alignment", "alignment": 5, "legacy": false},
            {"pos": [5, 18], "type": "position", "x": 175, "y": 460},
            {"pos": [18, 49], "type": "font-name", "name": "Utopia with Oldstyle figures"},
            {"pos": [49, 54], "type": "font-size", "size": 90},
            {"pos": [54, 60], "type": "border", "size": 0.0},
            {"pos": [60, 66], "type": "blur-edges-gauss", "value": 3.0},
            {"pos": [66, 78], "type": "color-primary", "red": 19, "green": 19, "blue": 19},
            {
                "pos": [78, 103],
                "type": "animation",
                "start": 0,
                "end": 1000,
                "accel": 2.0,
                "children":
                [
                    {"pos": [90, 102], "type": "color-primary", "red": 64, "green": 19, "blue": 19}
                ]
            },
            {
                "pos": [103, 137],
                "type": "animation",
                "start": 1000,
                "end": 2000,
                "accel": null,
                "children":
                [
                    {"pos": [116, 128], "type": "color-primary", "red": 178, "green": 21, "blue": 16},
                    {"pos": [128, 136], "type": "blur-edges-gauss", "value": 1.4}
                ]
            }
        ]
    },
    {"pos": [138, 150], "type": "text", "text": "Attack No. 1"},
    {
        "pos": [150, 165],
        "type": "tags",
        "children":
        [
            {"pos": [151, 164], "type": "comment", "text": "NOTE:\u30a2\u30bf\u30c3\u30afNo.1"}
        ]
    }
]
```

---

### Parsing draw tags

By default the content between `{\p1}` `{\p0}` is treated as plain text.  
However, you can pass it through `parse_draw_commands` function:

```python
from ass_tag_parser import parse_draw_commands
import json

result = parse_draw_commands('m 50 0 b 100 0 100 100 50 100 b 0 100 0 0 50 0')
print(json.dumps(result))
```

**Result**:

```json
[
    {"pos": [0, 6], "type": "move", "x": 50, "y": 0},
    {
        "pos": [7, 29],
        "type": "bezier",
        "points":
        [
            {"x": 100, "y": 0},
            {"x": 100, "y": 100},
            {"x": 50, "y": 100}
        ]
    },
    {
        "pos": [30, 46],
        "type": "bezier",
        "points":
        [
            {"x": 0, "y": 100},
            {"x": 0, "y": 0},
            {"x": 50, "y": 0}
        ]
    }
]
```

---

### Serializing the tree back

ASS tree: `serialize_ass`.  
Draw commands: `serialize_draw_commands`.

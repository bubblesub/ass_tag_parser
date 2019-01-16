import json

from ass_tag_parser import parse_ass, parse_draw_commands

result = parse_ass(
    r"{\an5\pos(175,460)\fnUtopia with Oldstyle figures\fs90\bord0\blur3"
    r"\1c&H131313&\t(0,1000,2,\1c&H131340&)\t(1000,2000,\1c&H1015B2&"
    r"\blur1.4)}Attack No. 1{NOTE:アタックNo.1}"
)
print(json.dumps(result, indent=4))

result = parse_draw_commands(r"m 50 0 b 100 0 100 100 50 100 b 0 100 0 0 50 0")
print(json.dumps(result, indent=4))

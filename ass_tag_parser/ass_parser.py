import typing as T
from dataclasses import dataclass

from ass_tag_parser.ass_struct import *
from ass_tag_parser.draw_parser import parse_draw_commands
from ass_tag_parser.errors import *
from ass_tag_parser.io import MyIO


@dataclass
class _ParseContext:
    io: MyIO
    drawing_tag: T.Optional[AssTagDraw] = None


def _single_arg(ctx: _ParseContext, tag: str) -> T.Tuple[T.Optional[str]]:
    arg = ""
    if ctx.io.peek(1) == "(":
        raise BadAssTagArgument(
            ctx.io.global_pos, f"{tag} doesn't take complex arguments"
        )
    while not ctx.io.eof and ctx.io.peek(1) not in r"\()":
        arg += ctx.io.read(1)
    if not arg:
        return (None,)
    return (arg,)


def _complex_args(
    ctx: _ParseContext, tag: str, valid_counts: T.Set[int]
) -> T.Tuple[T.Tuple[str, int], ...]:
    if ctx.io.read(1) != "(":
        raise BadAssTagArgument(ctx.io.global_pos, "expected brace")

    brackets = 1
    args: T.List[T.Tuple[str, int]] = []
    arg = ""
    arg_start = ctx.io.global_pos
    while brackets > 0:
        char = ctx.io.read(1)
        if char == "(":
            brackets += 1
            arg += char
        elif char == ")":
            brackets -= 1
            if brackets > 0:
                arg += char
            else:
                args.append((arg, arg_start))
                break
        elif char == ",":
            if brackets > 1:
                arg += char
            else:
                args.append((arg, arg_start))
                arg = ""
                arg_start = ctx.io.global_pos
        elif char in "{}":
            raise UnexpectedCurlyBrace(ctx.io.global_pos)
        elif ctx.io.eof:
            raise BadAssTagArgument(ctx.io.global_pos, "unterminated brace")
        else:
            arg += char

    if len(args) not in valid_counts:
        raise BadAssTagArgument(
            ctx.io.global_pos,
            f"{tag} takes {' or '.join(map(str, sorted(valid_counts)))} "
            f"arguments (got {len(args)})",
        )

    return tuple(args)


def _bool_arg(ctx: _ParseContext, tag: str) -> T.Tuple[T.Optional[bool]]:
    arg, = _single_arg(ctx, tag)
    if not arg:
        return (None,)
    if arg == "0":
        return (False,)
    if arg == "1":
        return (True,)
    raise BadAssTagArgument(ctx.io.global_pos, f"{tag} requires a boolean")


def _int_arg(ctx: _ParseContext, tag: str) -> T.Tuple[T.Optional[int]]:
    arg, = _single_arg(ctx, tag)
    if not arg:
        return (None,)
    try:
        return (int(arg),)
    except ValueError:
        raise BadAssTagArgument(
            ctx.io.global_pos, f"{tag} requires an integer"
        )


def _positive_int_arg(
    ctx: _ParseContext, tag: str
) -> T.Tuple[T.Optional[int]]:
    value, = _int_arg(ctx, tag)
    if value is not None and value < 0:
        raise BadAssTagArgument(
            ctx.io.global_pos, f"{tag} takes only positive integers"
        )
    return (value,)


def _float_arg(ctx: _ParseContext, tag: str) -> T.Tuple[T.Optional[float]]:
    arg, = _single_arg(ctx, tag)
    if not arg:
        return (None,)
    try:
        return (float(arg),)
    except ValueError:
        raise BadAssTagArgument(ctx.io.global_pos, f"{tag} requires a decimal")


def _positive_float_arg(
    ctx: _ParseContext, tag: str
) -> T.Tuple[T.Optional[float]]:
    value, = _float_arg(ctx, tag)
    if value is not None and value < 0:
        raise BadAssTagArgument(
            ctx.io.global_pos, f"{tag} takes only positive decimals"
        )
    return (value,)


def _pos_args(ctx: _ParseContext, tag: str) -> T.Tuple[float, float]:
    args = _complex_args(ctx, tag, {2})
    try:
        return tuple([float(item[0]) for item in args])
    except ValueError:
        raise BadAssTagArgument(
            ctx.io.global_pos, f"{tag} takes only decimal arguments"
        )


def _fade_simple_args(ctx: _ParseContext, tag: str) -> T.Tuple[float, float]:
    args = list(_complex_args(ctx, tag, {2}))

    try:
        args[0:2] = [float(item[0]) for item in args[0:2]]
        if any(arg < 0 for arg in args[0:2]):
            raise BadAssTagArgument(
                ctx.io.global_pos, f"{tag} takes only positive times"
            )
    except ValueError:
        raise BadAssTagArgument(
            ctx.io.global_pos, f"{tag} requires decimal times"
        )

    return tuple(args)


def _fade_complex_args(
    ctx: _ParseContext, tag: str
) -> T.Tuple[int, int, int, float, float, float, float]:
    args = list(_complex_args(ctx, tag, {7}))

    try:
        args[0:3] = [int(item[0]) for item in args[0:3]]
        if any(arg < 0 for arg in args[0:3]):
            raise BadAssTagArgument(
                ctx.io.global_pos, f"{tag} takes only positive alpha values"
            )
    except ValueError:
        raise BadAssTagArgument(
            ctx.io.global_pos, f"{tag} requires integer alpha values"
        )

    try:
        args[3:7] = [float(item[0]) for item in args[3:7]]
        if any(arg < 0 for arg in args[3:7]):
            raise BadAssTagArgument(
                ctx.io.global_pos, f"{tag} takes only positive times"
            )
    except ValueError:
        raise BadAssTagArgument(
            ctx.io.global_pos, f"{tag} requires decimal times"
        )

    return tuple(args)


def _bold_arg(
    ctx: _ParseContext, tag: str
) -> T.Tuple[T.Optional[bool], T.Optional[float]]:
    weight, = _positive_int_arg(ctx, tag)
    return (
        None if weight is None else weight != 0,
        None if weight is None or weight in {0, 1} else weight,
    )


def _alignment_arg(
    ctx: _ParseContext, tag: str
) -> T.Tuple[T.Optional[int], bool]:
    value, = _positive_int_arg(ctx, tag)
    legacy = tag == r"\a"
    if value is None:
        return (None, legacy)
    if legacy:
        if value in (1, 2, 3):
            pass
        elif value in (5, 6, 7):
            value -= 1
        elif value in (9, 10, 11):
            value -= 2
        else:
            raise BadAssTagArgument(
                ctx.io.global_pos, f"{tag} expects 1-3, 5-7 or 9-11"
            )
    elif value not in range(1, 10):
        raise BadAssTagArgument(ctx.io.global_pos, f"{tag} expects 1-9")
    return (value, legacy)


def _color_arg(
    ctx: _ParseContext, tag: str
) -> T.Tuple[T.Optional[int], T.Optional[int], T.Optional[int], int, bool]:
    start = ctx.io.global_pos
    arg, = _single_arg(ctx, tag)
    io = MyIO(arg or "", start, ctx.io.global_text)

    short = tag == r"\c"
    target = {r"\1c": 1, r"\2c": 2, r"\3c": 3, r"\4c": 4, r"\c": 1}[tag]
    if io.eof:
        return (None, None, None, target, short)

    if io.read(1) != "&":
        raise BadAssTagArgument(io.global_pos, "expected ampersand")
    if io.read(1) != "H":
        raise BadAssTagArgument(io.global_pos, "expected uppercase H")

    rgb = [0, 0, 0]
    for i in range(3):
        try:
            rgb[i] = int(io.read(2), 16)
        except ValueError:
            raise BadAssTagArgument(
                io.global_pos, "expected hexadecimal number"
            )

    if io.read(1) != "&":
        raise BadAssTagArgument(io.global_pos, "expected ampersand")

    if not io.eof:
        raise BadAssTagArgument(io.global_pos, "extra data")

    return (rgb[2], rgb[1], rgb[0], target, short)


def _alpha_arg(ctx: _ParseContext, tag: str) -> T.Tuple[T.Optional[int], int]:
    start = ctx.io.global_pos
    arg, = _single_arg(ctx, tag)
    io = MyIO(arg or "", start, ctx.io.global_text)

    target = {r"\1a": 1, r"\2a": 2, r"\3a": 3, r"\4a": 4, r"\alpha": 0}[tag]
    if io.peek(1) != "&":
        return (None, target)
    io.skip(1)

    if io.read(1) != "H":
        raise BadAssTagArgument(io.global_pos, "expected uppercase H")

    try:
        value = int(io.read(2), 16)
    except ValueError:
        raise BadAssTagArgument(io.global_pos, "expected hexadecimal number")

    if io.read(1) != "&":
        raise BadAssTagArgument(io.global_pos, "expected ampersand")

    if not io.eof:
        raise BadAssTagArgument(io.global_pos, "extra data")

    return (value, target)


def _karaoke_arg(ctx: _ParseContext, tag: str) -> T.Tuple[float, int]:
    karaoke_type = {"\\k": 1, "\\K": 2, "\\kf": 3, "\\ko": 4}[tag]
    value, = _positive_float_arg(ctx, tag)
    if value is None:
        raise BadAssTagArgument(
            ctx.io.global_pos, f"{tag} requires an argument"
        )
    return (value * 10, karaoke_type)


def _wrap_style_arg(ctx: _ParseContext, tag: str) -> T.Any:
    value, = _positive_int_arg(ctx, tag)
    if value not in range(4):
        raise BadAssTagArgument(
            ctx.io.global_pos, f"{tag} expects 0, 1, 2 or 3"
        )
    return (value,)


def _move_args(
    ctx: _ParseContext, tag: str
) -> T.Tuple[float, float, float, float, T.Optional[float], T.Optional[float]]:
    args = list(_complex_args(ctx, tag, {4, 6}))

    try:
        args[0:4] = [float(item[0]) for item in args[0:4]]
    except ValueError:
        raise BadAssTagArgument(
            ctx.io.global_pos, f"{tag} requires decimal coordinates"
        )

    if len(args) == 6:
        try:
            args[4:6] = [float(item[0]) for item in args[4:6]]
            if any(arg < 0 for arg in args[4:6]):
                raise BadAssTagArgument(
                    ctx.io.global_pos, f"{tag} takes only positive times"
                )
        except ValueError:
            raise BadAssTagArgument(
                ctx.io.global_pos, f"{tag} requires decimal times"
            )

    return args


def _animation_args(
    ctx: _ParseContext, tag: str
) -> T.Tuple[
    T.List[AssTag], T.Optional[float], T.Optional[float], T.Optional[float]
]:
    acceleration: T.Union[None, str, float]
    time1: T.Union[None, str, float]
    time2: T.Union[None, str, float]
    tags: T.Union[None, str, T.List[AssTag]]

    args = _complex_args(ctx, tag, {1, 2, 3, 4})

    if len(args) == 1:
        acceleration = None
        time1 = None
        time2 = None
        tags, tags_start = args[0]
    elif len(args) == 2:
        acceleration = args[0][0]
        time1 = None
        time2 = None
        tags, tags_start = args[1]
    elif len(args) == 3:
        acceleration = None
        time1 = args[0][0]
        time2 = args[1][0]
        tags, tags_start = args[2]
    else:
        time1 = args[0][0]
        time2 = args[1][0]
        acceleration = args[2][0]
        tags, tags_start = args[3]

    try:
        acceleration = None if acceleration is None else float(acceleration)
    except ValueError:
        raise BadAssTagArgument(
            ctx.io.global_pos, f"{tag} requires decimal acceleration value"
        )
    if acceleration is not None and acceleration < 0:
        raise BadAssTagArgument(
            ctx.io.global_pos, f"{tag} takes only positive acceleration value"
        )

    try:
        time1 = None if time1 is None else float(time1)
        time2 = None if time2 is None else float(time2)
    except ValueError:
        raise BadAssTagArgument(
            ctx.io.global_pos, f"{tag} requires decimal times"
        )
    if (time1 is not None and time1 < 0) or (time2 is not None and time2 < 0):
        raise BadAssTagArgument(
            ctx.io.global_pos, f"{tag} takes only positive times"
        )

    old_io = ctx.io
    ctx.io = MyIO(tags, tags_start, ctx.io.global_text)
    tags = list(_parse_ass_tags(ctx))
    ctx.io = old_io

    return tags, time1, time2, acceleration


_PARSING_MAP = [
    (r"\bord", AssTagBorder, _positive_float_arg),
    (r"\xbord", AssTagXBorder, _positive_float_arg),
    (r"\ybord", AssTagYBorder, _positive_float_arg),
    (r"\shad", AssTagShadow, _positive_float_arg),
    (r"\xshad", AssTagXShadow, _positive_float_arg),
    (r"\yshad", AssTagYShadow, _positive_float_arg),
    (r"\fsp", AssTagLetterSpacing, _float_arg),
    (r"\fax", AssTagXShear, _float_arg),
    (r"\fay", AssTagYShear, _float_arg),
    (r"\pos", AssTagPosition, _pos_args),
    (r"\org", AssTagRotationOrigin, _pos_args),
    (r"\move", AssTagMove, _move_args),
    (r"\fade", AssTagFadeComplex, _fade_complex_args),
    (r"\fad", AssTagFade, _fade_simple_args),
    (r"\frx", AssTagXRotation, _float_arg),
    (r"\fry", AssTagYRotation, _float_arg),
    (
        r"\frz",
        AssTagZRotation,
        lambda ctx, tag: tuple(list(_float_arg(ctx, tag)) + [False]),
    ),
    (
        r"\fr",
        AssTagZRotation,
        lambda ctx, tag: tuple(list(_float_arg(ctx, tag)) + [True]),
    ),
    (r"\fn", AssTagFontName, _single_arg),
    (r"\fscx", AssTagFontXScale, _positive_float_arg),
    (r"\fscy", AssTagFontYScale, _positive_float_arg),
    (r"\fs", AssTagFontSize, _positive_int_arg),
    (r"\fe", AssTagFontEncoding, _positive_int_arg),
    (r"\blur", AssTagBlurEdgesGauss, _positive_float_arg),
    (r"\be", AssTagBlurEdges, _positive_int_arg),
    (r"\i", AssTagItalic, _bool_arg),
    (r"\u", AssTagUnderline, _bool_arg),
    (r"\s", AssTagStrikeout, _bool_arg),
    (r"\b", AssTagBold, _bold_arg),
    (r"\kf", AssTagKaraoke, _karaoke_arg),
    (r"\ko", AssTagKaraoke, _karaoke_arg),
    (r"\k", AssTagKaraoke, _karaoke_arg),
    (r"\K", AssTagKaraoke, _karaoke_arg),
    (r"\q", AssTagWrapStyle, _wrap_style_arg),
    (r"\r", AssTagResetStyle, _single_arg),
    (r"\alpha", AssTagAlpha, _alpha_arg),
    (r"\1a", AssTagAlpha, _alpha_arg),
    (r"\2a", AssTagAlpha, _alpha_arg),
    (r"\3a", AssTagAlpha, _alpha_arg),
    (r"\4a", AssTagAlpha, _alpha_arg),
    (r"\1c", AssTagColor, _color_arg),
    (r"\2c", AssTagColor, _color_arg),
    (r"\3c", AssTagColor, _color_arg),
    (r"\4c", AssTagColor, _color_arg),
    (r"\c", AssTagColor, _color_arg),
    (r"\an", AssTagAlignment, _alignment_arg),
    (r"\a", AssTagAlignment, _alignment_arg),
    (r"\pbo", AssTagBaselineOffset, _float_arg),
    (r"\p", AssTagDraw, _positive_int_arg),
    (r"\t", AssTagAnimation, _animation_args),
]


def _parse_ass_tag(ctx: _ParseContext) -> AssTag:
    i = ctx.io.global_pos

    for prefix in {r"\clip", r"\iclip"}:
        if ctx.io.peek(len(prefix)) != prefix:
            continue
        ctx.io.skip(len(prefix))
        inverse = prefix == r"\iclip"
        args = _complex_args(ctx, prefix, {1, 2, 4})

        if len(args) == 1:
            scale = None
            path = args[0][0]
            return AssTagClipVector(
                scale=scale, path=parse_draw_commands(path), inverse=inverse
            )

        elif len(args) == 2:
            scale = args[0][0]
            path = args[1][0]
            try:
                scale = int(scale)
            except ValueError:
                raise BadAssTagArgument(
                    ctx.io.global_pos, f"{prefix} scale must be integer"
                )
            if scale < 0:
                raise BadAssTagArgument(
                    ctx.io.global_pos,
                    f"{prefix} scale must be positive integer",
                )
            return AssTagClipVector(
                scale=scale, path=parse_draw_commands(path), inverse=inverse
            )

        elif len(args) == 4:
            try:
                corners = [float(arg[0]) for arg in args]
            except ValueError:
                raise BadAssTagArgument(
                    ctx.io.global_pos,
                    f"{prefix} takes only decimal coordinates",
                )
            return AssTagClipRectangle(
                corners[0], corners[1], corners[2], corners[3], inverse=inverse
            )

        else:
            assert False

    for prefix, cls, arg_func in _PARSING_MAP:
        if ctx.io.peek(len(prefix)) == prefix:
            ctx.io.skip(len(prefix))
            args = arg_func(ctx, prefix)
            ret: AssTag = cls(*args)
            ret.meta = Meta(
                i, ctx.io.global_pos, ctx.io.global_text[i : ctx.io.global_pos]
            )

            if (
                isinstance(ret, AssTagDraw)
                and ret.scale is not None
                and ret.scale > 0
            ):
                ctx.drawing_tag = ret

            return ret

    raise UnknownTag(ctx.io.global_pos)


def _merge_comments(tags: T.List[AssTag]) -> T.List[AssTag]:
    if not tags:
        return []

    ret = [tags.pop(0)]
    while tags:
        cur = tags.pop(0)

        if isinstance(ret[-1], AssTagComment) and isinstance(
            cur, AssTagComment
        ):
            prev = ret.pop()
            assert cur.meta
            assert prev.meta
            assert isinstance(prev, AssTagComment)
            block = AssTagComment(prev.text + cur.text)
            block.meta = Meta(prev.meta.start, cur.meta.end, block.text)
            ret.append(block)
        else:
            ret.append(cur)

    return ret


def _parse_ass_tags(ctx: _ParseContext) -> T.Iterable[AssTag]:
    while not ctx.io.eof:
        if ctx.io.peek(1) == "\\":
            if ctx.io.peek(2) in {r"\N", r"\n", r"\h", r"\\"}:
                block = AssTagComment(ctx.io.read(2))
                block.meta = Meta(
                    ctx.io.global_pos, ctx.io.global_pos + 2, block.text
                )
                yield block
            else:
                yield _parse_ass_tag(ctx)
        else:
            i = ctx.io.global_pos
            while not ctx.io.eof and ctx.io.peek(1) != "\\":
                ctx.io.skip(1)
            j = ctx.io.global_pos
            block = AssTagComment(ctx.io.global_text[i:j])
            block.meta = Meta(i, j, block.text)
            yield block


def _parse_ass(ctx: _ParseContext) -> T.Iterable[AssItem]:
    while not ctx.io.eof:
        i = ctx.io.pos
        if ctx.io.peek(1) == "{":

            ctx.io.skip(1)
            while True:
                if ctx.io.eof:
                    raise UnterminatedCurlyBrace(ctx.io.global_pos)
                if ctx.io.peek(1) == "{":
                    raise UnexpectedCurlyBrace(ctx.io.global_pos)
                if ctx.io.peek(1) == "}":
                    ctx.io.skip(1)
                    break
                ctx.io.skip(1)
            j = ctx.io.pos

            tag_list_opening = AssTagListOpening()
            tag_list_opening.meta = Meta(i, i + 1, "{")
            yield tag_list_opening

            old_io = ctx.io
            ctx.io = ctx.io.divide(i + 1, j - 1)
            yield from _merge_comments(list(_parse_ass_tags(ctx)))
            ctx.io = old_io

            tag_list_ending = AssTagListEnding()
            tag_list_ending.meta = Meta(j - 1, j, "}")
            yield tag_list_ending

        else:
            while not ctx.io.eof:
                if ctx.io.peek(1) == "{":
                    break
                elif ctx.io.peek(1) == "}":
                    raise UnexpectedCurlyBrace(ctx.io.global_pos)
                ctx.io.skip(1)
            j = ctx.io.pos
            text = ctx.io.text[i:j]
            if ctx.drawing_tag is not None:
                ctx.drawing_tag.path = parse_draw_commands(text)
                ctx.drawing_tag = None
            else:
                text = AssText(text)
                text.meta = Meta(i, j, ctx.io.text[i:j])
                yield text


def parse_ass(text: str) -> T.List[AssItem]:
    ctx = _ParseContext(io=MyIO(text))
    return list(_parse_ass(ctx))

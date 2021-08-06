from dataclasses import dataclass

from ass_tag_parser.ass_struct import (
    AssItem,
    AssTag,
    AssTagAlignment,
    AssTagAlpha,
    AssTagAnimation,
    AssTagBaselineOffset,
    AssTagBlurEdges,
    AssTagBlurEdgesGauss,
    AssTagBold,
    AssTagBorder,
    AssTagClipRectangle,
    AssTagClipVector,
    AssTagColor,
    AssTagComment,
    AssTagDraw,
    AssTagFade,
    AssTagFadeComplex,
    AssTagFontEncoding,
    AssTagFontName,
    AssTagFontSize,
    AssTagFontXScale,
    AssTagFontYScale,
    AssTagItalic,
    AssTagKaraoke,
    AssTagLetterSpacing,
    AssTagListEnding,
    AssTagListOpening,
    AssTagMove,
    AssTagPosition,
    AssTagResetStyle,
    AssTagRotationOrigin,
    AssTagShadow,
    AssTagStrikeout,
    AssTagUnderline,
    AssTagWrapStyle,
    AssTagXBorder,
    AssTagXRotation,
    AssTagXShadow,
    AssTagXShear,
    AssTagYBorder,
    AssTagYRotation,
    AssTagYShadow,
    AssTagYShear,
    AssTagZRotation,
    AssText,
)
from ass_tag_parser.common import smart_bool, smart_float, smart_int, smart_str
from ass_tag_parser.draw_composer import compose_draw_commands
from ass_tag_parser.io import MyIO


@dataclass
class _ComposeContext:
    io: MyIO
    autoinsert: bool
    opened: bool = False


def visitor(ctx: _ComposeContext, item: AssItem) -> None:
    # pylint: disable=too-many-statements,too-many-branches

    if isinstance(item, AssTag) and ctx.autoinsert and not ctx.opened:
        ctx.io.write("{")
        ctx.opened = True
    elif isinstance(item, AssText) and ctx.autoinsert and ctx.opened:
        ctx.io.write("}")
        ctx.opened = False

    if isinstance(item, AssTagListOpening):
        if not ctx.autoinsert:
            ctx.io.write("{")
    elif isinstance(item, AssTagListEnding):
        if not ctx.autoinsert:
            ctx.io.write("}")

    elif isinstance(item, AssTagAnimation):
        ctx.io.write("\\t(")
        if item.time1 is not None and item.time2 is not None:
            ctx.io.write(
                f"{smart_float(item.time1)},{smart_float(item.time2)},"
            )
        if item.acceleration is not None:
            ctx.io.write(f"{smart_float(item.acceleration)},")
        for subitem in item.tags:
            visitor(ctx, subitem)
        ctx.io.write(")")

    elif isinstance(item, AssText):
        ctx.io.write(item.text)
    elif isinstance(item, AssTagComment):
        ctx.io.write(f"{item.text}")
    elif isinstance(item, AssTagBaselineOffset):
        ctx.io.write(f"\\pbo{smart_float(item.y)}")
    elif isinstance(item, AssTagDraw):
        ctx.io.write(f"\\p{smart_int(item.scale)}")
        ctx.io.write("}")
        ctx.io.write(compose_draw_commands(item.path))
        ctx.io.write("{\\p0")
    elif isinstance(item, AssTagAlignment):
        if item.legacy:
            value = item.alignment
            if value in {4, 5, 6}:
                value += 1
            elif value in {7, 8, 9}:
                value += 2
            ctx.io.write(f"\\a{smart_int(value)}")
        else:
            ctx.io.write(f"\\an{smart_int(item.alignment)}")
    elif isinstance(item, AssTagFade):
        ctx.io.write("\\fad(")
        ctx.io.write(f"{smart_float(item.time1)},{smart_float(item.time2)}")
        ctx.io.write(")")
    elif isinstance(item, AssTagFadeComplex):
        ctx.io.write("\\fade(")
        ctx.io.write(f"{item.alpha1},{item.alpha2},{item.alpha3},")
        ctx.io.write(f"{smart_float(item.time1)},{smart_float(item.time2)},")
        ctx.io.write(f"{smart_float(item.time3)},{smart_float(item.time4)}")
        ctx.io.write(")")
    elif isinstance(item, AssTagMove):
        ctx.io.write("\\move(")
        ctx.io.write(f"{smart_float(item.x1)},{smart_float(item.y1)},")
        ctx.io.write(f"{smart_float(item.x2)},{smart_float(item.y2)}")
        if item.time1 is not None and item.time2 is not None:
            ctx.io.write(
                f",{smart_float(item.time1)},{smart_float(item.time2)}"
            )
        ctx.io.write(")")
    elif isinstance(item, AssTagColor):
        ctx.io.write("\\c" if item.short else f"\\{item.target}c")
        if (
            item.red is not None
            and item.green is not None
            and item.blue is not None
        ):
            ctx.io.write("&H")
            ctx.io.write(f"{item.blue:02X}")
            ctx.io.write(f"{item.green:02X}")
            ctx.io.write(f"{item.red:02X}")
            ctx.io.write("&")
    elif isinstance(item, AssTagAlpha):
        ctx.io.write("\\alpha" if item.target == 0 else f"\\{item.target}a")
        if item.value is not None:
            ctx.io.write("&H")
            ctx.io.write(f"{item.value:02X}")
            ctx.io.write("&")
    elif isinstance(item, AssTagResetStyle):
        ctx.io.write(f"\\r{smart_str(item.style)}")
    elif isinstance(item, AssTagBorder):
        ctx.io.write(f"\\bord{smart_float(item.size)}")
    elif isinstance(item, AssTagXBorder):
        ctx.io.write(f"\\xbord{smart_float(item.size)}")
    elif isinstance(item, AssTagYBorder):
        ctx.io.write(f"\\ybord{smart_float(item.size)}")
    elif isinstance(item, AssTagShadow):
        ctx.io.write(f"\\shad{smart_float(item.size)}")
    elif isinstance(item, AssTagXShadow):
        ctx.io.write(f"\\xshad{smart_float(item.size)}")
    elif isinstance(item, AssTagYShadow):
        ctx.io.write(f"\\yshad{smart_float(item.size)}")
    elif isinstance(item, AssTagXRotation):
        ctx.io.write(f"\\frx{smart_float(item.angle)}")
    elif isinstance(item, AssTagYRotation):
        ctx.io.write(f"\\fry{smart_float(item.angle)}")
    elif isinstance(item, AssTagZRotation):
        ctx.io.write(
            f"\\fr{smart_float(item.angle)}"
            if item.short
            else f"\\frz{smart_float(item.angle)}"
        )
    elif isinstance(item, AssTagRotationOrigin):
        ctx.io.write(f"\\org({smart_float(item.x)},{smart_float(item.y)})")
    elif isinstance(item, AssTagPosition):
        ctx.io.write(f"\\pos({smart_float(item.x)},{smart_float(item.y)})")
    elif isinstance(item, AssTagXShear):
        ctx.io.write(f"\\fax{smart_float(item.value)}")
    elif isinstance(item, AssTagYShear):
        ctx.io.write(f"\\fay{smart_float(item.value)}")
    elif isinstance(item, AssTagFontName):
        ctx.io.write(f"\\fn{smart_str(item.name)}")
    elif isinstance(item, AssTagFontSize):
        ctx.io.write(f"\\fs{smart_int(item.size)}")
    elif isinstance(item, AssTagFontEncoding):
        ctx.io.write(f"\\fe{smart_int(item.encoding)}")
    elif isinstance(item, AssTagLetterSpacing):
        ctx.io.write(f"\\fsp{smart_float(item.spacing)}")
    elif isinstance(item, AssTagFontXScale):
        ctx.io.write(f"\\fscx{smart_float(item.scale)}")
    elif isinstance(item, AssTagFontYScale):
        ctx.io.write(f"\\fscy{smart_float(item.scale)}")
    elif isinstance(item, AssTagBlurEdges):
        ctx.io.write(f"\\be{smart_float(item.times)}")
    elif isinstance(item, AssTagBlurEdgesGauss):
        ctx.io.write(f"\\blur{smart_float(item.weight)}")
    elif isinstance(item, AssTagKaraoke):
        tag = {1: "\\k", 2: "\\K", 3: "\\kf", 4: "\\ko"}[item.karaoke_type]
        ctx.io.write(f"{tag}{smart_float(item.duration / 10)}")
    elif isinstance(item, AssTagItalic):
        ctx.io.write(f"\\i{smart_bool(item.enabled)}")
    elif isinstance(item, AssTagUnderline):
        ctx.io.write(f"\\u{smart_bool(item.enabled)}")
    elif isinstance(item, AssTagStrikeout):
        ctx.io.write(f"\\s{smart_bool(item.enabled)}")
    elif isinstance(item, AssTagWrapStyle):
        ctx.io.write(f"\\q{smart_int(item.style)}")
    elif isinstance(item, AssTagBold):
        ctx.io.write(
            "\\b"
            + (
                str(item.weight)
                if item.weight is not None
                else smart_bool(item.enabled)
            )
        )
    elif isinstance(item, AssTagClipRectangle):
        ctx.io.write("\\iclip" if item.inverse else "\\clip")
        ctx.io.write(f"({smart_float(item.x1)},{smart_float(item.y1)},")
        ctx.io.write(f"{smart_float(item.x2)},{smart_float(item.y2)})")
    elif isinstance(item, AssTagClipVector):
        ctx.io.write("\\iclip" if item.inverse else "\\clip")
        ctx.io.write("(")
        if item.scale is not None:
            ctx.io.write(f"{item.scale},")
        ctx.io.write(compose_draw_commands(item.path))
        ctx.io.write(")")
    else:
        raise NotImplementedError(f"not implemented ({type(item)})")


def compose_ass(ass_line: list[AssItem], autoinsert: bool = True) -> str:
    ctx = _ComposeContext(io=MyIO(), autoinsert=autoinsert)

    for item in ass_line:
        visitor(ctx, item)

    if ctx.opened:
        ctx.io.write("}")
    return ctx.io.text

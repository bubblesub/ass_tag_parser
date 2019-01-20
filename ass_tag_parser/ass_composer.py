import contextlib

from ass_tag_parser.ass_struct import *
from ass_tag_parser.io import MyIO


def walk_ass_line_ctx(
    ass_line: AssLine, visit: T.Callable[[AssItem], T.Iterator[None]]
) -> None:
    def walk_items(items: T.Sequence[AssItem]) -> None:
        for item in items:
            with visit(item):
                if isinstance(item, (AssTagList, AssTagAnimation)):
                    walk_items(item.tags)

    walk_items(ass_line.chunks)


def walk_ass_line(
    ass_line: AssLine, visit: T.Callable[[AssItem], None]
) -> None:
    def walk_items(items: T.Sequence[AssItem]) -> None:
        for item in items:
            visit(item)
            if isinstance(item, (AssTagList, AssTagAnimation)):
                walk_items(item.tags)

    walk_items(ass_line.chunks)


@contextlib.contextmanager
def visitor(text_io: MyIO, item: AssItem) -> T.Iterator[None]:
    if isinstance(item, AssTagList):
        text_io.write("{")
        yield
        text_io.write("}")
        return

    if isinstance(item, AssTagAnimation):
        text_io.write("\\t(")
        if item.acceleration is not None:
            if item.time1 is not None and item.time2 is not None:
                text_io.write(
                    f"{item.time1},{item.time2},{item.acceleration},"
                )
            else:
                text_io.write(f"{item.acceleration},")
        elif item.time1 is not None and item.time2 is not None:
            text_io.write(f"{item.time1},{item.time2},")
        yield
        text_io.write(")")
        return

    if isinstance(item, AssText):
        text_io.write(item.text)
    elif isinstance(item, AssTagComment):
        text_io.write(f"{item.text}")
    elif isinstance(item, AssTagBaselineOffset):
        text_io.write(f"\\pbo{item.y}")
    elif isinstance(item, AssTagDrawingMode):
        text_io.write(f"\\p{item.scale}")
    elif isinstance(item, AssTagAlignment):
        if item.legacy:
            value = item.alignment
            if value in {4, 5, 6}:
                value += 1
            elif value in {7, 8, 9}:
                value += 2
            text_io.write(f"\\a{value}")
        else:
            text_io.write(f"\\an{item.alignment}")
    elif isinstance(item, AssTagFade):
        text_io.write(f"\\fad({item.time1},{item.time2})")
    elif isinstance(item, AssTagFadeComplex):
        text_io.write("\\fade(")
        text_io.write(f"{item.alpha1},{item.alpha2},{item.alpha3},")
        text_io.write(f"{item.time1},{item.time2},{item.time3},{item.time4}")
        text_io.write(")")
    elif isinstance(item, AssTagMove):
        text_io.write("\\move(")
        text_io.write(f"{item.x1},{item.y1},{item.x2},{item.y2}")
        if item.time1 is not None and item.time2 is not None:
            text_io.write(f",{item.time1},{item.time2}")
        text_io.write(")")
    elif isinstance(item, AssTagColor):
        text_io.write("\\c" if item.short else f"\\{item.target}c")
        if (
            item.red is not None
            and item.green is not None
            and item.blue is not None
        ):
            text_io.write("&H")
            text_io.write(f"{item.blue:02X}")
            text_io.write(f"{item.green:02X}")
            text_io.write(f"{item.red:02X}")
            text_io.write("&")
    elif isinstance(item, AssTagAlpha):
        text_io.write("\\alpha" if item.target == 0 else f"\\{item.target}a")
        if item.value is not None:
            text_io.write("&H")
            text_io.write(f"{item.value:02X}")
            text_io.write("&")
    elif isinstance(item, AssTagResetStyle):
        text_io.write(f"\\r{item.style or ''}")
    elif isinstance(item, AssTagBorder):
        text_io.write(f"\\bord{item.size}")
    elif isinstance(item, AssTagXBorder):
        text_io.write(f"\\xbord{item.size}")
    elif isinstance(item, AssTagYBorder):
        text_io.write(f"\\ybord{item.size}")
    elif isinstance(item, AssTagShadow):
        text_io.write(f"\\shad{item.size}")
    elif isinstance(item, AssTagXShadow):
        text_io.write(f"\\xshad{item.size}")
    elif isinstance(item, AssTagYShadow):
        text_io.write(f"\\yshad{item.size}")
    elif isinstance(item, AssTagXRotation):
        text_io.write(f"\\frx{item.angle}")
    elif isinstance(item, AssTagYRotation):
        text_io.write(f"\\fry{item.angle}")
    elif isinstance(item, AssTagZRotation):
        text_io.write(
            f"\\fr{item.angle}" if item.short else f"\\frz{item.angle}"
        )
    elif isinstance(item, AssTagRotationOrigin):
        text_io.write(f"\\org({item.x},{item.y})")
    elif isinstance(item, AssTagPosition):
        text_io.write(f"\\pos({item.x},{item.y})")
    elif isinstance(item, AssTagXShear):
        text_io.write(f"\\fax{item.value}")
    elif isinstance(item, AssTagYShear):
        text_io.write(f"\\fay{item.value}")
    elif isinstance(item, AssTagFontName):
        text_io.write(f"\\fn{item.name}")
    elif isinstance(item, AssTagFontSize):
        text_io.write(f"\\fs{item.size}")
    elif isinstance(item, AssTagFontEncoding):
        text_io.write(f"\\fe{item.encoding}")
    elif isinstance(item, AssTagLetterSpacing):
        text_io.write(f"\\fsp{item.spacing}")
    elif isinstance(item, AssTagFontXScale):
        text_io.write(f"\\fscx{item.scale}")
    elif isinstance(item, AssTagFontYScale):
        text_io.write(f"\\fscy{item.scale}")
    elif isinstance(item, AssTagBlurEdges):
        text_io.write(f"\\be{item.times}")
    elif isinstance(item, AssTagBlurEdgesGauss):
        text_io.write(f"\\blur{item.weight}")
    elif isinstance(item, AssTagKaraoke1):
        text_io.write(f"\\k{item.duration // 10}")
    elif isinstance(item, AssTagKaraoke2):
        text_io.write(f"\\K{item.duration // 10}")
    elif isinstance(item, AssTagKaraoke3):
        text_io.write(f"\\kf{item.duration // 10}")
    elif isinstance(item, AssTagKaraoke4):
        text_io.write(f"\\ko{item.duration // 10}")
    elif isinstance(item, AssTagItalic):
        text_io.write("\\i" + ("1" if item.enabled else "0"))
    elif isinstance(item, AssTagUnderline):
        text_io.write("\\u" + ("1" if item.enabled else "0"))
    elif isinstance(item, AssTagStrikeout):
        text_io.write("\\s" + ("1" if item.enabled else "0"))
    elif isinstance(item, AssTagWrapStyle):
        text_io.write(f"\\q{item.style}")
    elif isinstance(item, AssTagBold):
        text_io.write(
            "\\b"
            + (
                str(item.weight)
                if item.weight is not None
                else ("1" if item.enabled else "0")
            )
        )
    elif isinstance(item, AssTagClipRectangle):
        text_io.write("\\iclip" if item.inverse else "\\clip")
        text_io.write(f"({item.x1},{item.y1},{item.x2},{item.y2})")
    elif isinstance(item, AssTagClipVector):
        text_io.write("\\iclip" if item.inverse else "\\clip")
        text_io.write("(")
        if item.scale is not None:
            text_io.write(f"{item.scale},")
        text_io.write(f"{item.path})")
    else:
        raise NotImplementedError("not implemented")

    yield


def compose_ass(ass_line: AssLine) -> str:
    text_io = MyIO()
    walk_ass_line_ctx(ass_line, lambda item: visitor(text_io, item))
    return text_io.text

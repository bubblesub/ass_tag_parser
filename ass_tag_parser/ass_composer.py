from ass_tag_parser.common import ParsingError


def byte(value):
    ret = int(value)
    if ret not in range(256):
        raise ValueError("Invalid byte value {}".format(ret))
    return ret


def smart_float(value):
    return "{}".format(float(value)).rstrip("0").rstrip(".")


class Serializer:
    def visit(self, tree):
        ret = ""
        for item in tree:
            if "type" not in item:
                raise ParsingError("Item has no type")

            visitor = getattr(
                self, "visit_" + item["type"].replace("-", "_"), None
            )
            if not visitor:
                raise ParsingError("Unknown type %r" % item["type"])

            try:
                result = visitor(item)
            except (IndexError, KeyError, ValueError, TypeError) as ex:
                raise ParsingError(ex)

            ret += result
        return ret

    def visit_text(self, item):
        return item["text"]

    def visit_tags(self, item):
        ret = ""
        for subitem in item["children"]:
            ret += self.visit_ass_tag(subitem)
        return "{" + ret + "}"

    def visit_ass_tag(self, item):
        if "type" not in item:
            raise ParsingError("Item has no type")

        visitor = getattr(
            self, "visit_ass_tag_" + item["type"].replace("-", "_"), None
        )
        if not visitor:
            raise ParsingError("Unknown tag %r" % item["type"])

        try:
            result = visitor(item)
        except (IndexError, KeyError, ValueError, TypeError) as ex:
            raise ParsingError(ex)

        return result

    def visit_ass_tag_comment(self, item):
        return item["text"]

    def visit_ass_tag_italics(self, item):
        return r"\i{}".format(1 if item["enabled"] else 0)

    def visit_ass_tag_bold(self, item):
        return r"\b{}".format(
            item["weight"]
            if "weight" in item
            else (1 if item["enabled"] else 0)
        )

    def visit_ass_tag_underline(self, item):
        return r"\u{}".format(1 if item["enabled"] else 0)

    def visit_ass_tag_strikeout(self, item):
        return r"\s{}".format(1 if item["enabled"] else 0)

    def visit_ass_tag_border(self, item):
        value = float(item["size"])
        if value < 0:
            raise ValueError("Border size cannot be negative")
        return r"\bord{}".format(smart_float(value))

    def visit_ass_tag_border_x(self, item):
        value = float(item["size"])
        if value < 0:
            raise ValueError("Border size cannot be negative")
        return r"\xbord{}".format(smart_float(value))

    def visit_ass_tag_border_y(self, item):
        value = float(item["size"])
        if value < 0:
            raise ValueError("Border size cannot be negative")
        return r"\ybord{}".format(smart_float(value))

    def visit_ass_tag_shadow(self, item):
        value = float(item["size"])
        if value < 0:
            raise ValueError("Shadow size cannot be negative")
        return r"\shad{}".format(smart_float(value))

    def visit_ass_tag_shadow_x(self, item):
        value = float(item["size"])
        if value < 0:
            raise ValueError("Shadow size cannot be negative")
        return r"\xshad{}".format(smart_float(value))

    def visit_ass_tag_shadow_y(self, item):
        value = float(item["size"])
        if value < 0:
            raise ValueError("Shadow size cannot be negative")
        return r"\yshad{}".format(smart_float(value))

    def visit_ass_tag_blur_edges(self, item):
        value = int(item["value"])
        if value < 0:
            raise ValueError("Blur weight cannot be negative")
        return r"\be{}".format(value)

    def visit_ass_tag_blur_edges_gauss(self, item):
        value = float(item["value"])
        if value < 0:
            raise ValueError("Blur weight cannot be negative")
        return r"\blur{}".format(smart_float(value))

    def visit_ass_tag_font_name(self, item):
        return r"\fn({})".format(item["name"])

    def visit_ass_tag_font_encoding(self, item):
        value = item["encoding"]
        if value < 0:
            raise ValueError("Invalid font encoding")
        return r"\fe{}".format(value)

    def visit_ass_tag_font_size(self, item):
        value = int(item["size"])
        if value < 0:
            raise ValueError("Font size cannot be negative")
        return r"\fs{}".format(value)

    def visit_ass_tag_font_scale_x(self, item):
        value = float(item["scale"])
        if value < 0:
            raise ValueError("Font scale cannot be negative")
        return r"\fscx{}".format(smart_float(value))

    def visit_ass_tag_font_scale_y(self, item):
        value = float(item["scale"])
        if value < 0:
            raise ValueError("Font scale cannot be negative")
        return r"\fscy{}".format(smart_float(value))

    def visit_ass_tag_letter_spacing(self, item):
        value = float(item["value"])
        return r"\fsp{}".format(value)

    def visit_ass_tag_rotation_x(self, item):
        value = float(item["angle"])
        return r"\frx{}".format(smart_float(value))

    def visit_ass_tag_rotation_y(self, item):
        value = float(item["angle"])
        return r"\fry{}".format(smart_float(value))

    def visit_ass_tag_rotation_z(self, item):
        value = float(item["angle"])
        return r"\frz{}".format(smart_float(value))

    def visit_ass_tag_rotation_origin(self, item):
        return r"\org({},{})".format(int(item["x"]), int(item["y"]))

    def visit_ass_tag_shear_x(self, item):
        value = float(item["value"])
        return r"\fax{}".format(value)

    def visit_ass_tag_shear_y(self, item):
        value = float(item["value"])
        return r"\fay{}".format(value)

    def visit_ass_tag_color_primary(self, item):
        return r"\1c&H{:02X}{:02X}{:02X}&".format(
            byte(item["blue"]), byte(item["green"]), byte(item["red"])
        )

    def visit_ass_tag_color_secondary(self, item):
        return r"\2c&H{:02X}{:02X}{:02X}&".format(
            byte(item["blue"]), byte(item["green"]), byte(item["red"])
        )

    def visit_ass_tag_color_border(self, item):
        return r"\3c&H{:02X}{:02X}{:02X}&".format(
            byte(item["blue"]), byte(item["green"]), byte(item["red"])
        )

    def visit_ass_tag_color_shadow(self, item):
        return r"\4c&H{:02X}{:02X}{:02X}&".format(
            byte(item["blue"]), byte(item["green"]), byte(item["red"])
        )

    def visit_ass_tag_alpha_all(self, item):
        return r"\alpha&H{:02X}&".format(byte(item["value"]))

    def visit_ass_tag_alpha_primary(self, item):
        return r"\1a&H{:02X}&".format(byte(item["value"]))

    def visit_ass_tag_alpha_secondary(self, item):
        return r"\2a&H{:02X}&".format(byte(item["value"]))

    def visit_ass_tag_alpha_border(self, item):
        return r"\3a&H{:02X}&".format(byte(item["value"]))

    def visit_ass_tag_alpha_shadow(self, item):
        return r"\4a&H{:02X}&".format(byte(item["value"]))

    def visit_ass_tag_karaoke_1(self, item):
        value = int(item["duration"]) // 10
        if value < 0:
            raise ValueError("Karaoke duration cannot be negative")
        return r"\k{}".format(value)

    def visit_ass_tag_karaoke_2(self, item):
        value = int(item["duration"]) // 10
        if value < 0:
            raise ValueError("Karaoke duration cannot be negative")
        return r"\K{}".format(value)

    def visit_ass_tag_karaoke_3(self, item):
        value = int(item["duration"]) // 10
        if value < 0:
            raise ValueError("Karaoke duration cannot be negative")
        return r"\kf{}".format(value)

    def visit_ass_tag_karaoke_4(self, item):
        value = int(item["duration"]) // 10
        if value < 0:
            raise ValueError("Karaoke duration cannot be negative")
        return r"\ko{}".format(value)

    def visit_ass_tag_alignment(self, item):
        value = int(item["alignment"])
        legacy = bool(item["legacy"])
        if value not in range(1, 10):
            raise ValueError("Invalid alignment value")
        if legacy:
            if value in (4, 5, 6):
                value += 1
            elif value in (7, 8, 9):
                value += 2
            return r"\a{}".format(value)
        return r"\an{}".format(value)

    def visit_ass_tag_wrap_style(self, item):
        value = int(item["value"])
        if value not in range(4):
            raise ValueError("Invalid wrap style")
        return r"\q{}".format(value)

    def visit_ass_tag_reset_style(self, item):
        value = item["style"] or ""
        return r"\r{}".format(value)

    def visit_ass_tag_position(self, item):
        x = int(item["x"])
        y = int(item["y"])
        return r"\pos({},{})".format(x, y)

    def visit_ass_tag_movement(self, item):
        x1 = int(item["x1"])
        y1 = int(item["y1"])
        x2 = int(item["x2"])
        y2 = int(item["y2"])
        start = int(item["start"]) if item["start"] is not None else None
        end = int(item["end"]) if item["end"] is not None else None
        if (start is None) != (end is None):
            raise ValueError(
                "Movement start and end time must be both provided "
                "or both omitted"
            )
        if start is not None and (start < 0 or end < 0):
            raise ValueError("Movement time cannot be negative")
        if start is None:
            return r"\move({},{},{},{})".format(x1, y1, x2, y2)
        return r"\move({},{},{},{},{},{})".format(x1, y1, x2, y2, start, end)

    def visit_ass_tag_fade_simple(self, item):
        start = int(item["start"])
        end = int(item["end"])
        if start < 0 or end < 0:
            raise ValueError("Fade time cannot be negative")
        return r"\fad({},{})".format(start, end)

    def visit_ass_tag_fade_complex(self, item):
        alpha1 = byte(item["alpha1"])
        alpha2 = byte(item["alpha2"])
        alpha3 = byte(item["alpha3"])
        time1 = int(item["time1"])
        time2 = int(item["time2"])
        time3 = int(item["time3"])
        time4 = int(item["time4"])
        if time1 < 0 or time2 < 0 or time3 < 0 or time4 < 0:
            raise ValueError("Fade time cannot be negative")
        return r"\fade({},{},{},{},{},{},{})".format(
            alpha1, alpha2, alpha3, time1, time2, time3, time4
        )

    def visit_ass_tag_animation(self, item):
        start = int(item["start"]) if item["start"] is not None else None
        end = int(item["end"]) if item["end"] is not None else None
        accel = float(item["accel"]) if item["accel"] is not None else None
        if (start is None) != (end is None):
            raise ValueError(
                "Animation start and end time must be both provided "
                "or both omitted"
            )
        if start is not None and (start < 0 or end < 0):
            raise ValueError("Animation time cannot be negative")

        tags = "".join(
            self.visit_ass_tag(subitem) for subitem in item["children"]
        )

        if start is not None and accel is not None:
            return r"\t({},{},{},{})".format(start, end, accel, tags)
        elif start is not None and accel is None:
            return r"\t({},{},{})".format(start, end, tags)
        elif start is None and accel is not None:
            return r"\t({},{})".format(accel, tags)
        else:
            return r"\t({})".format(tags)

    def visit_ass_tag_clip_rectangle(self, item):
        x1 = int(item["x1"])
        y1 = int(item["y1"])
        x2 = int(item["x2"])
        y2 = int(item["y2"])
        inverse = bool(item["inverse"])
        return r"\{}clip({},{},{},{})".format(
            "i" if inverse else "", x1, y1, x2, y2
        )

    def visit_ass_tag_clip_vector(self, item):
        scale = float(item["scale"]) if item["scale"] is not None else None
        inverse = bool(item["inverse"])
        commands = item["commands"]
        ret = r"\{}clip".format("i" if inverse else "")
        if scale is not None:
            ret += "({},{})".format(smart_float(scale), commands)
        else:
            ret += "({})".format(commands)
        return ret

    def visit_ass_tag_drawing_mode(self, item):
        value = int(item["value"])
        return r"\p{}".format(value)

    def visit_ass_tag_baseline_offset(self, item):
        value = int(item["value"])
        return r"\pbo{}".format(value)


def compose_ass(tree):
    return Serializer().visit(tree)

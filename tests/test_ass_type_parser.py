from ass_tag_analyzer.ass_type_parser import TypeParser


def test_color_arg():
    assert TypeParser.color_arg(int("FA9632", 16)) == (50, 150, 250)


def test_float_str_to_float():

    # Whitespace and invalid text
    assert TypeParser.float_str_to_float(" \t\v20.39445InvalidText") == 20.39445

    # Invalid text at the beginning
    assert TypeParser.float_str_to_float("InvalidText-20") == 0

    # Multiple dot
    assert TypeParser.float_str_to_float("20.39.445") == 20.39

    # One dot without number
    assert TypeParser.float_str_to_float("20.") == 20

    # Multiple +-
    assert TypeParser.float_str_to_float("+-20.39.445") == 0

    # Integer
    assert TypeParser.float_str_to_float("20") == 20

    # +-
    assert TypeParser.float_str_to_float("+20") == 20
    assert TypeParser.float_str_to_float("-20") == -20

    # Exponent
    assert TypeParser.float_str_to_float("2e+2") == 2 * pow(10, 2)
    assert TypeParser.float_str_to_float("2e-2") == 2 * pow(10, -2)
    assert TypeParser.float_str_to_float("2e2") == 2 * pow(10, 2)
    assert TypeParser.float_str_to_float("2e") == 2
    assert TypeParser.float_str_to_float("2.e10") == 2 * pow(10, 10)
    assert TypeParser.float_str_to_float("e10") == 0


def test_int_str_to_int():

    # Whitespace and invalid text
    assert TypeParser.int_str_to_int("\t\v20.39445InvalidText") == 20

    # Invalid text at the beginning
    assert TypeParser.int_str_to_int("InvalidText-20") == 0

    # Multiple dot
    assert TypeParser.int_str_to_int("20.39.445") == 20

    # Multiple +-
    assert TypeParser.int_str_to_int("+-20.39.445") == 0

    # Integer
    assert TypeParser.int_str_to_int("20") == 20

    # +-
    assert TypeParser.int_str_to_int("+20") == 20
    assert TypeParser.int_str_to_int("-20") == -20


def test_hex_str_to_int():

    # Whitespace and invalid text
    assert TypeParser.hex_str_to_int("\t\v6BInvalidText") == 107

    # Invalid text at the beginning
    assert TypeParser.hex_str_to_int("InvalidText-20") == 0

    # Multiple dot
    assert TypeParser.hex_str_to_int("6B.39.445") == 107

    # Multiple +-
    assert TypeParser.hex_str_to_int("+-6B.39.445") == 0

    # Integer
    assert TypeParser.hex_str_to_int("6B") == 107

    # +-
    assert TypeParser.hex_str_to_int("+6B") == 107
    assert TypeParser.hex_str_to_int("-6B") == -107

    # With lowercase characters
    assert TypeParser.hex_str_to_int("-6b") == -107

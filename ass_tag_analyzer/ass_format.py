class Format:
    @staticmethod
    def _format_float(number: float) -> str:
        """
        Parameters:
            number (float): An float.
        Returns:
            The float converted to string.

            Ex:
                - 4.3004 --> "4.3"
                - 4.0054 --> "4.005"
                - 4.0056 --> "4.006"
        """
        return "{:.3f}".format(number).rstrip("0").rstrip(".")

    """
    All float tag like \\blur, \\be, \\fax, etc use this variable.
    If you wanna change how ass_tag_analyzer converted them into string, then you need to redefine format_float

    Ex:
        def my_new_way_to_format_float(number: float) -> str:
            return YOUR_WAY_TO_CONVERT_FLOAT_TO_STRING
        
        Format.format_float = my_new_way_to_format_float
    """
    format_float = _format_float

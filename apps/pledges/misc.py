from string import Formatter


def get_var_names_from_string_format(str_format):
    return [var_name for _, var_name, _, _ in Formatter().parse(str_format)]
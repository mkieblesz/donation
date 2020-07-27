from apps.pledges.misc import get_var_names_from_string_format


def test_get_var_names_from_string_format():
    assert get_var_names_from_string_format('my name is {name} lol {number:.2f}') == [
        'name',
        'number',
    ]
    assert get_var_names_from_string_format('') == []

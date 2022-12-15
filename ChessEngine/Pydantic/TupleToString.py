from typing import Tuple, Any, cast


def string_to_tuple(value: str) -> Tuple[Any]:
    value.replace('(', '')
    value.replace(')', '')
    return cast(Tuple[Any], tuple(value.split(',')))

def tuple_to_string(tup: Tuple[int, int]) -> str:
    return_string = ''
    tup_len = len(tup)
    for index, item in enumerate(tup):
        if index == tup_len - 1:
            return_string += f'{item}'
        else:
            return_string += f'{item}, '
    return f'({return_string})'


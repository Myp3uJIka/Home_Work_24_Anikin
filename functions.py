from classes import DataRequest, DataRequestSchema
from werkzeug.exceptions import BadRequest
from typing import Tuple, Optional

import re

AVAILABLE_COMMANDS = 'Available commands: filter, map, unique, sort, limit.'


def check_query(req: dict) -> Tuple[str, str, str, str, str]:
    """Проверка наличия требуемых параметров в запросе включая проверку наличия файла для обработки"""
    data: DataRequest = DataRequestSchema().load(req)
    return data.file_name, data.cmd1, data.value1, data.cmd2, data.value2


def req_filter(value: str, data: list) -> list:
    """Фильтрация по наличию ключевого слова"""
    return list(filter(lambda l: value in l, [line for line in data]))


def req_map(value: str, data: list) -> list:
    """Выделение нужной колонки из строки"""
    return list(map(lambda l: l[int(value)], [line.split() for line in data if len(line) > 0]))


def req_unique(data: list) -> list:
    """Сбор уникальных значений"""
    res = [line for line in data]
    return list(set(res))


def req_sort(value: str, data: list) -> list:
    """Сортировка значений по алфавиту, или в обратном порядке"""
    rev = True if value == 'desc' else False
    return sorted([line for line in data], reverse=rev)


def req_limit(value: str, data: list) -> list:
    """Вывод ограниченного количества строк"""
    return [line for line in data][:int(value)]


def req_regex(value: str, data: list) -> list:
    """Вывод совпадений согласно регулярному выражению"""
    regex = re.compile(value)
    match_lines = (line for line in data if regex.findall(line))
    return [line for line in match_lines]


def processing(cmd: str, value: str, data: list) -> list:
    """Вызов функции для обработки согласно указанному параметру cmd"""
    if cmd == 'filter':
        return req_filter(value, data)
    elif cmd == 'map':
        return req_map(value, data)
    elif cmd == 'unique':
        return req_unique(data)
    elif cmd == 'sort':
        return req_sort(value, data)
    elif cmd == 'limit':
        return req_limit(value, data)
    elif cmd == 'regex':
        return req_regex(value, data)
    else:
        raise BadRequest(description=f'{cmd} is not defined. {AVAILABLE_COMMANDS}')

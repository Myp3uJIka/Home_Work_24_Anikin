from flask import request
from werkzeug.exceptions import BadRequest

AVAILABLE_COMMANDS = 'Available commands: filter, map, unique, sort, limit.'


def check_query():
    """Проверка наличия требуемых параметров в запросе включая проверку наличия файла для обработки"""
    req = request.json
    file_name = req['file_name']
    cmd1 = req['cmd1']
    value1 = req['value1']
    cmd2 = req['cmd2']
    value2 = req['value2']

    return file_name, cmd1, value1, cmd2, value2


def req_filter(value, data):
    """Фильтрация по наличию ключевого слова"""
    return list(filter(lambda l: value in l, [line for line in data]))


def req_map(value, data):
    """Выделение нужной колонки из строки"""
    return list(map(lambda l: l[int(value)], [line.split() for line in data if len(line) > 0]))


def req_unique(data):
    """Сбор уникальных значений"""
    res = [line for line in data]
    return set(res)


def req_sort(value, data):
    """Сортировка значений по алфавиту, или в обратном порядке"""
    if value == 'desc':
        return sorted([line for line in data], reverse=True)
    else:
        return sorted([line for line in data], reverse=False)


def req_limit(value, data):
    """Вывод ограниченного количества строк"""
    return [line for line in data][:int(value)]


def processing(cmd, value, data):
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
    else:
        raise BadRequest(description=f'{cmd} is not defined. {AVAILABLE_COMMANDS}')

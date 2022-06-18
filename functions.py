import os

from flask import request


def check_query(DATA_DIR):  # наличия требуемых параметров в запросе включая проверку наличия файла для обработки
    try:
        req = request.json
        file_name = req['file_name']
        cmd1 = req['cmd1']
        value1 = req['value1']
        cmd2 = req['cmd2']
        value2 = req['value2']

        file_path = os.path.join(DATA_DIR, file_name)
        if not os.path.exists(file_path):
            return f'{file_name} was not found'
        return file_path, file_name, cmd1, value1, cmd2, value2

    except KeyError:
        return f'one or more parameters was not defined'


def req_filter(value, data):  # фильтрация по наличию ключевого слова
    return list(filter(lambda l: value in l, [line for line in data]))


def req_map(value, data):  # выделение нужной колонки из строки
    return list(map(lambda l: l[int(value)], [line.split() for line in data if len(line) > 0]))


def req_unique(data):  # сбор уникальных значений
    res = [line for line in data]
    return set(res)


def req_sort(value, data):  # сортировка значений по алфавиту, или в обратном порядке
    if value == 'desc':
        return sorted([line for line in data], reverse=True)
    else:
        return sorted([line for line in data], reverse=False)


def req_limit(value, data):  # вывод ограниченного количества строк
    return [line for line in data][:int(value)]


def processing(cmd, value, data):  # вызов функции для обработки согласно указанному параметру cmd
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
        return f'{cmd} is not defined'

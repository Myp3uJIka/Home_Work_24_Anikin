import os

from flask import Flask, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query", methods=['POST'])
def perform_query():
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат

    req = request.json

    try:
        file_name = req['file_name']
        cmd1 = req['cmd1']
        value1 = req['value1']
        cmd2 = req['cmd2']
        value2 = req['value2']
    except Exception as e:
        return f'bad request - {e}', 400

    try:
        with open(os.path.join(DATA_DIR, file_name), 'r', encoding='utf-8') as f:
            response_data = f.read().split('\n')

    except Exception as e:
        return f'bad request - {e}', 400

    def req_filter(value, data):
        return list(filter(lambda l: value in l, [line for line in data]))

    def req_map(value, data):
        return list(map(lambda l: l[int(value)], [line.split() for line in data if len(line) > 0]))

    def req_unique(data):
        res = [line for line in data]
        return set(res)

    def req_sort(value, data):
        if value == 'desc':
            return sorted([line for line in data], reverse=True)
        else:
            return sorted([line for line in data], reverse=False)

    def req_limit(value, data):
        res = []
        cnt = 1
        for line in data:
            res.append(line)
            cnt += 1
            if cnt > int(value):
                return res

    def operation(cmd, value, data):
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
            raise ValueError

    res_cmd1 = operation(cmd1, value1, response_data)
    res_cmd2 = operation(cmd2, value2, res_cmd1)

    res_cmd2 = '\n'.join(res_cmd2)
    # return res_cmd2

    return app.response_class(res_cmd2, content_type="text/plain")


if __name__ == '__main__':
    app.run(host='localhost', port=10001, debug=True)

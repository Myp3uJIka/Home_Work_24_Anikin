import os


from flask import Flask, request
from werkzeug.exceptions import BadRequest

from functions import req_limit, req_map, req_sort, req_unique, req_filter

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query", methods=['POST'])
def perform_query():
    """
    Вью обрабатывает запрос на примере из req.http. Применяет обработку к текстовому файлу пяти видов: filter, map,
    unique, sort, limit.
    :return: результат обработки двух команд (cmd1 & cmd2)
    """

    try:
        req = request.json
        file_name = req['file_name']
        cmd1 = req['cmd1']
        value1 = req['value1']
        cmd2 = req['cmd2']
        value2 = req['value2']

        file_path = os.path.join(DATA_DIR, file_name)
        if not os.path.exists(file_path):
            return BadRequest(description=f'{file_path} was not found')

    except KeyError:
        raise BadRequest

    with open(file_path, 'r', encoding='utf-8') as f:
        response_data = f.read().split('\n')

    def processing(cmd, value, data):
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
            raise BadRequest

    res_cmd1 = processing(cmd1, value1, response_data)
    res_cmd2 = processing(cmd2, value2, res_cmd1)

    content = '\n'.join(res_cmd2)

    return app.response_class(content, content_type="text/plain")


if __name__ == '__main__':
    app.run(host='localhost', port=10001, debug=True)

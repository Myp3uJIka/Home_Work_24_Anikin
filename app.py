import os

from flask import Flask, request, Response
from werkzeug.exceptions import BadRequest
from typing import Optional, Dict, Any

from functions import check_query, processing

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
        file_name, cmd1, value1, cmd2, value2 = check_query(request.json)
    except KeyError as e:
        raise BadRequest(description=f'Not found: {e}')

    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        raise BadRequest(description=f'{file_name} was not found')

    with open(file_path, 'r', encoding='utf-8') as f:
        response_data = f.read().split('\n')
    try:
        res_cmd1 = processing(cmd1, value1, response_data)
        res_cmd2 = processing(cmd2, value2, res_cmd1)
    except BadRequest as e:
        raise BadRequest(description=e)

    content = '\n'.join(res_cmd2)

    return app.response_class(content, content_type="text/plain")


if __name__ == '__main__':
    app.run(host='localhost', port=10001, debug=True)

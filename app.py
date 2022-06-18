import os


from flask import Flask, request
from werkzeug.exceptions import BadRequest

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

    # проверка корректности запроса
    if 'one or more parameters was not defined' in check_query(DATA_DIR):
        raise BadRequest(description=check_query(DATA_DIR))
    elif f'{request.json["file_name"]} was not found' in check_query(DATA_DIR):
        raise BadRequest(description=check_query(DATA_DIR))
    else:
        file_path, file_name, cmd1, value1, cmd2, value2 = check_query(DATA_DIR)

    with open(file_path, 'r', encoding='utf-8') as f:
        response_data = f.read().split('\n')

    # запуск обработки
    if f'{request.json["cmd1"]} is not defined' in processing(cmd1, value1, response_data):
        raise BadRequest(description=processing(cmd1, value1, response_data))
    else:
        res_cmd1 = processing(cmd1, value1, response_data)

    if f'{request.json["cmd2"]} is not defined' in processing(cmd2, value2, res_cmd1):
        raise BadRequest(description=processing(cmd2, value2, res_cmd1))
    else:
        res_cmd2 = processing(cmd2, value2, res_cmd1)

    content = '\n'.join(res_cmd2)

    return app.response_class(content, content_type="text/plain")


if __name__ == '__main__':
    app.run(host='localhost', port=10001, debug=True)

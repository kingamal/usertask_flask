import requests
from flask import Flask, send_file
import http.client


URL_USERS = "https://jsonplaceholder.typicode.com/users"
URL_TODOS = "https://jsonplaceholder.typicode.com/todos"


def response(url):
    responses = requests.request("GET", url)
    responses = responses.json()
    return responses


users = response(URL_USERS)
todos = response(URL_TODOS)


app = Flask(__name__)
conn = http.client.HTTPSConnection("localhost", 8080)


@app.route('/')
def homepage():
    return f"<h2> Plik dostępny pod adresem " \
           f"<a href='http://127.0.0.1:8080/app/user_task'> http://127.0.0.1:8080/app/user_task</a></h2>"


@app.route('/app/user_task')
def user_task():
    response = send_file(
        path_or_file="file.csv",
        as_attachment=True,
    )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

import requests
from flask import Flask, send_file
import http.client
import sqlite3
import csv


URL_USERS = "https://jsonplaceholder.typicode.com/users"
URL_TODOS = "https://jsonplaceholder.typicode.com/todos"


def get_responses(url):
    responses = requests.request("GET", url)
    responses = responses.json()
    return responses


def making_db():
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    return conn, cur


def users_in_db():
    users = get_responses(URL_USERS)
    conn, cur = making_db()
    cur.executescript("""
        DROP TABLE IF EXISTS users;
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY ASC,
            name varchar(250) NOT NULL,
            username varchar(250) NOT NULL,
            email varchar(250) NOT NULL,
            address_street varchar(250) NOT NULL,
            address_suite varchar(250) NOT NULL,
            address_city varchar(250) NOT NULL,
            address_zipcode varchar(250) NOT NULL,
            address_geo_lat varchar(250) NOT NULL,
            address_geo_lng varchar(250) NOT NULL,
            phone varchar(250) NOT NULL,
            website varchar(250) NOT NULL,
            company_name varchar(250) NOT NULL,
            company_catchPhrase TEXT NOT NULL,
            company_bs varchar(250) NOT NULL
        )""")

    val = ()
    for i in users:
        val = (i['id'], i['name'], i['username'], i['email'], i['address']['street'], i['address']['suite'],
               i['address']['city'], i['address']['zipcode'], i['address']['geo']['lat'], i['address']['geo']['lng'],
               i['phone'], i['website'], i['company']['name'], i['company']['catchPhrase'], i['company']['bs'])
        cur.executemany('INSERT INTO users VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (val,))
        conn.commit()


def todos_in_db():
    todos = get_responses(URL_TODOS)
    conn, cur = making_db()
    cur.executescript("""
        DROP TABLE IF EXISTS todos;
        CREATE TABLE IF NOT EXISTS todos (
            todos_id INTEGER PRIMARY KEY ASC,
            title varchar(250) NOT NULL,
            completed varchar(250) NOT NULL,
            users_id INTEGER NOT NULL,
            FOREIGN KEY(users_id) REFERENCES users(user_id)
        )""")

    val2 = ()
    for i in todos:
        val2 = (i['id'], i['title'], i['completed'], i['userId'])
        cur.executemany('INSERT INTO todos VALUES(?,?,?,?)', (val2,))
        conn.commit()


def export_to_csv():
    conn, cur = making_db()
    users_in_db()
    todos_in_db()
    cur.execute(
        """
        SELECT name, address_city, title, completed FROM users, todos
        WHERE users.user_id=todos.users_id
    """)
    user_task = cur.fetchall()
    with open("user_task.csv", "w", newline="") as fp:
        fpwriter = csv.writer(fp)
        fpwriter.writerow(["name", "city", "title", "completed"])
        for task in user_task:
            fpwriter.writerow(task)


export_to_csv()


app = Flask(__name__)
conn = http.client.HTTPSConnection("localhost", 8080)


@app.route('/')
def homepage():
    return f"<h2> Plik dostępny pod adresem " \
           f"<a href='http://127.0.0.1:8080/app/user_task'> http://127.0.0.1:8080/app/user_task</a></h2>"


@app.route('/app/user_task')
def user_task():
    response = send_file(
        path_or_file="user_task.csv",
        as_attachment=True,
    )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

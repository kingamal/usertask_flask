import sqlite3
from main import users, todos

# print(users)

conn = sqlite3.connect('test.db')
cur = conn.cursor()

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

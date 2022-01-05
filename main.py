import requests

url_users = "https://jsonplaceholder.typicode.com/users"
url_todos = "https://jsonplaceholder.typicode.com/todos"


def response(url):
    responses = requests.request("GET", url)
    responses = responses.json()
    return print(responses)


response(url_users)
response(url_todos)

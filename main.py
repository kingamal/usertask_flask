import requests


URL_USERS = "https://jsonplaceholder.typicode.com/users"
URL_TODOS = "https://jsonplaceholder.typicode.com/todos"


def response(url):
    responses = requests.request("GET", url)
    responses = responses.json()
    return responses


users = response(URL_USERS)
todos = response(URL_TODOS)

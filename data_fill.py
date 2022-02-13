import requests
import random


def fill_users():
    for i in range(10):
        rand = random.randint(1, 10000)
        data = {
            "email": f"example{rand}@example.ru",
            "password": "examplepass123",
            "password2": "examplepass123",
            "is_author": "true" if rand > 5000 else "false"
        }
        requests.post("https://presentsite.herokuapp.com/api/register", data=data)
        if rand > 5000:
            data = {
                "article_title": f"Example Title - {rand}",
                "article_text": f"Big Example Article - {rand}",
                "is_public": "true"
            }
            headers = {"Authorization": {"username": f"example{rand}@example.ru", "password": "examplepass123"}}

        q = requests.post("https://presentsite.herokuapp.com/api/articles/create",
                      data=data,
                      auth=(f"example{rand}@example.ru", "examplepass123")
                      )
        print(q)


fill_users()

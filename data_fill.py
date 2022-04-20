import requests
import random


def fill_users():
    for i in range(10):
        rand = random.randint(1, 10000)
        data = {
            "email": f"example{rand}@example.ru",
            "password": "examplepass123",
            "password2": "examplepass123",
            "username": f"user{rand}"
        }
        resp = requests.post("http://127.0.0.1:3000/api/user/register", data=data)
        print(resp)
        token = resp.text[10:resp.text.find('\",\"user')]

        data = {
            "age": random.randint(18, 50),
            "first_name": "first_name",
            "last_name": "last_name",
            "latitude": random.randint(537522, 577522) / 10000,
            "longitude": random.randint(356156, 396156) / 10000,
            "is_author": True,
            "sex": True if random.randint(0, 1) == 0 else False
        }
        q = requests.patch("http://127.0.0.1:3000/api/user/cabinet",
                           data=data,
                           headers={"Authorization": f"Token  {token}"}
                           )
        print(q)


# №55.7522°, 376156°
fill_users()

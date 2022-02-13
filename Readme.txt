git clone git@github.com:sovius23/fortest.git main
Для запуска:
-Необходим PostgreSQL!
1.Создать базу данных и внести изменения в файл testsite/settings.py в DATABASE
2.Установить все модули -команда pip install -r requirements.txt (или pip3)
3.Применить миграции python manage.py migrate (или pip3)
Запуск командой python manage.py runserver 3000 (или любой другой порт) (или python3)

Либо через docker в ветке docker_branch:
1.docker-compose build
2.docker-compose up
3.адрес http://localhost:3000/

Heroku-развертка: https://presentsite.herokuapp.com/  - возможно потребуется время для запуска сервера,около 5 сек.

Работает визуальное представление на DRF - для удобства добавлена SessionAuthentication

Действующие адреса:

"/api/register"
"/api/login" (имеют смысл при SessionAuthentication)
"/api/logout" (имеют смысл при SessionAuthentication)
"/api/cabinet"
"/api/articles/public"
"/api/articles/create"
"/api/articles/edit/<int:pk>"

API:

"/api/register"

POST:{
    "email":"example.example.ru",    -Валидация на соответствие email,неповторимости и заполнения поля
    "password":"example123",    -Валидация на заполнения поля, размер более 8 символов, присутствие одной буквы, одной цифры
    "password2":"example123",    -Валидация на соответствие первому паролю
    "is_author":"true/false"    хочет ли пользователь быть автором
}
    Если все успешно - ответ "Signed in!"

"/api/login"

POST:{
    "email":"example.example.ru",    -Валидация на соответствие email,неповторимости и заполнения поля
    "password":"example123",    -Валидация на заполнения поля, размер более 8 символов, присутствие одной буквы, одной цифры
}
    Если все успешно - ответ "Successfull login!"

"/api/logout"

GET: требует заголовок "Authorization":{"username":"example.example.ru","password":"example123"}
Возвращает "Successfull logout!"

"/api/cabinet"
требует заголовок "Authorization":{"username":"example.example.ru","password":"example123"}

доступны методы GET - возвращает пользователя по Авторизации
PATCH - изменяет пользователя по Авторизации

PATCH: пример тела -{
    "is_author": true,
    "is_subscriber": true,
    "is_active": true,    - для "выключения" пользователя
    "password":"newPassword123"
}
DELETE - удаляет пользователя по Авторизации

"/api/articles/public"

GET:
если есть заголовок "Authorization":{"username":"example.example.ru","password":"example123"},
то возвращает все статьи.
если нет-только публичные

"/api/articles/create"
требует заголовок "Authorization":{"username":"example.example.ru","password":"example123"}
GET-все статьи пользователя
POST - создание новой статьи, если пользователь is_author
пример тела : {
    "article_title": "Example Title",
    "article_text": " Big Example Article",
    "is_public": false
}

"/api/articles/edit/<int:pk>"
требует заголовок "Authorization":{"username":"example.example.ru","password":"example123"}
доступны методы GET - возвращает статью по номеру <int:pk> после проверки прав на нее
PATCH- изменяет статью по номеру <int:pk> после проверки прав на нее
PATCH: пример тела -{
    "id": 2,
    "article_title": "example",
    "article_text": "Big Example Article",
    "user_id": 4,
    "is_public": false
}
DELETE - даляет статью по номеру <int:pk> после проверки прав на нее

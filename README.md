# Проект "Продуктовый помощник"
____
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.
____
## Технологии:
Python 3.9, Django 3.2, DRF, JWT, PostgreSQL, Docker, nginx, gunicorn.
Проект написан в операционной системе Windows. Запускается в четырёх контейнерах:
- infra_db_1 - postgres:13.0-alpine
- infra_web_1 - foodgram_backend
- infra_nginx_1 - nginx:1.19.3
- infra_frontend_1 - foodgram_frontend
____
## Как запустить проект(все команды выполняются в командной оболочке bach):
1. Клонировать репозиторий и перейти в него в командной строке.
2. Создать и активировать виртуальное окружение
3. Установить зависимости командой: 
```
pip install -r requirements.txt
```
4. В папке infra/ создать файл .env с переменными окружения, необходимыми для работы приложения.
### Пример содержимого файла:
```
SECRET_KEY=секретный ключ Django
DEBUG=False
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
### SECRET_KEY можно сгенерировать из директории backend/
### Для этого необходимо выполнить поочередно команды:
```
python manage.py shell
from django.core.management.utils import get_random_secret_key  
get_random_secret_key()
```
После этого, полученный код скопировать в .env
5. В папке infra/ выполнить команду для сборки контейнеров
```
docker-compose up
```
____
## Примеры запросов к API

### Список пользователей
```
GET /api/users/
```
Ответ:
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/?page=4",
  "previous": "http://foodgram.example.org/api/users/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": false
    }
  ]
}
```
### Регистрация пользователя
```
POST /api/users/
```
```
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}
```
Ответ:
```
{
  "email": "vpupkin@yandex.ru",
  "id": 0,
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин"
}
```
### Получить токен авторизации
Используется для авторизации по емейлу и паролю, чтобы далее использовать токен при запросах.
```
POST /api/auth/token/login/
```
```
{
  "password": "string",
  "email": "string"
}
```
Ответ:
```
{
  "auth_token": "string"
}
```
### Cписок тегов
```
GET api/tags/
```
Ответ:
```
[
  {
    "id": 0,
    "name": "Завтрак",
    "color": "#E26C2D",
    "slug": "breakfast"
  }
]
```
### Создание рецепта
Доступно только авторизованному пользователю
```
POST /api/recipes/
```
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
Ответ:
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```
### Добавить рецепт в список покупок
Доступно только авторизованным пользователям
```
POST /api/recipes/{id}/shopping_cart/
```
Ответ:
```
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}
```
### Добавить рецепт в избранное
Доступно только авторизованному пользователю.
```
POST /api/recipes/{id}/favorite/
```
Ответ:
```
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}
```
### Мои подписки
Возвращает пользователей, на которых подписан текущий пользователь. В выдачу добавляются рецепты.
```
GET /api/users/subscriptions/
```
Ответ:
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/subscriptions/?page=4",
  "previous": "http://foodgram.example.org/api/users/subscriptions/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": true,
      "recipes": [
        {
          "id": 0,
          "name": "string",
          "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
          "cooking_time": 1
        }
      ],
      "recipes_count": 0
    }
  ]
}
```
### Подписаться на пользователя
Доступно только авторизованным пользователям
```
POST /api/users/{id}/subscribe/
```
Ответ:
```
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": true,
  "recipes": [
    {
      "id": 0,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "cooking_time": 1
    }
  ],
  "recipes_count": 0
}
```
### Список ингредиентов
Список ингредиентов с возможностью поиска по имени.
```
GET /api/ingredients/
```
Ответ:
```
[
  {
    "id": 0,
    "name": "Капуста",
    "measurement_unit": "кг"
  }
]
```
### Полная окументация API доступна по адресу
```
http://localhost/api/docs/
```
### Проект доступен по адресу
```
http://foodgram-roev.ddns.net
```
```
Администратор: admin
E-mail: admin@admin.ru
password: qwerty1234567890
```
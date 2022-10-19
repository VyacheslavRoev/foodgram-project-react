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
### Документация API доступна по адресу
```
http://localhost/api/docs/
```
### Проект доступен по адресу
```
http://foodgram-roev.ddns.net
```

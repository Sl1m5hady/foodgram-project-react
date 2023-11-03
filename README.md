## Проект Foodgram - Продуктовый помощник

Позволяет делиться рецептами с другими пользователями, добавлять в рецепты в избранное.
Есть возможность подписок и добавления рецептов в список покупок, который можно скачать.


### Технологии:

Python, Django, DRF, Docker, Gunicorn, NGINX, PostgreSQL, 

### Развернуть проект на удаленном сервере:

- Клонировать репозиторий:
```
https://github.com/sl1m5hady/foodgram-project-react.git
```

- Установить Docker Compose


- Скопировать на сервер docker-compose.production.yml, nginx.conf


- Запустить контейнеры
```
sudo docker compose -f docker-compose.production.yml up -d
```

- Создать суперпользователя:
```
sudo docker compose exec backend python manage.py createsuperuser
```


- Наполнить базу ингредиентами:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py ingredients
```

- Для остановки сервиса:
```
sudo docker compose -f docker-compose.production.yml stop
```

- Для удаления контейнеров:
```
sudo docker compose-f docker-compose.production.yml down
```

# Foodgram
![Python version](https://img.shields.io/badge/python-3.9-yellow) ![Django version](https://img.shields.io/badge/django-3.2-red)

![workflow](https://github.com/HelloAgni/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

Сервис "Продуктовый помощник". На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Технологии

- [Python](https://www.python.org/) 3.9+
- [django](https://github.com/django/django) 3.2
- [django-rest-framework](https://github.com/encode/django-rest-framework)
  3.14

## Запуск проекта в dev режиме

Клонировать репозиторий, перейти в папку с бэкендом, установить и активировать виртуальное окружение

```
cd backend
python -m venv venv
# mac/linux
source venv/bin/activate
# win
source venv/Scripts/activate 
``` 

Установить зависимости из файла requirements.txt

```
pip install -r requirements.txt
``` 

Выполнить миграции, импортировать ингредиенты и запустить проект

```
python manage.py migrate
python manage.py ingredients data/ingredients.csv
python manage.py runserver
``` 

## Запуск проекта в docker контейнере

Клонировать репозиторий и перейти в foodgram-project-react/infra/

```bash
git clone https://github.com/GoodLifeSeeker/foodgram-project-react.git
cd foodgram-project-react/infra/
``` 

Клонировать [образец](/infra/example.env) файла переменного окружения и заполнить по необходимости

```bash
cp example.env .env
``` 

Развернуть docker контейнеры. Миграции и сбор статики производятся автоматически

```
docker-compose up -d
``` 

Создать суперпользователя

```bash
docker-compose exec web python manage.py createsuperuser
```

Импортировать ингредиенты

```bash
docker-compose exec web python manage.py ingredients data/ingredients.csv
```

Проект станет доступен по адресу `http://localhost/`

## Примеры запросов к API

Список запросов можно посмотреть перейдя на `http://localhost/api/docs/` развернутого проекта

## Автор
[Алексей Вьюник](https://github.com/GoodLifeSeeker)

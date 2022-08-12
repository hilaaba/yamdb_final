# YaMDb API 
---
![yamdb workflow](https://github.com/hilaaba/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Адрес сервера
http://84.201.162.16/redoc/

## Краткое описание проекта YaMDb
Проект YaMDb собирает отзывы пользователей на произведения.
Произведения делятся на категории: "Книги", "Фильмы", "Музыка".
Список категорий может быть расширен администратором
(например, можно добавить категорию "Ювелирные изделия").
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведению может быть присвоен жанр из списка.
Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти;
из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число).
На одно произведение пользователь может оставить только один отзыв.

## Технологии
![gunicorn](https://img.shields.io/badge/gunicorn-blue) ![Nginx](https://img.shields.io/badge/Nginx-blue) ![Docker](https://img.shields.io/badge/Docker-blue) ![Docker-compose](https://img.shields.io/badge/Docker--compose-blue) 

## Шаблон наполнения env-файла
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

## Запуск контейнера и приложения в нем

Перейти в репозиторий для запуска докера

```
cd infra/
```

Запуск docker-compose

```
docker-compose up -d --build
```

Выполните по очереди команды:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

Загрузите подготовленные данные в базу данных:

```
docker-compose exec web python manage.py loaddata fixtures.json
```

## Некоторые примеры запросов к API

### Cписок всех произведений
GET /api/v1/titles/

### Cписок всех отзывов
GET /api/v1/titles/{title_id}/reviews/

### Добавить новый отзыв
POST /api/v1/titles/{title_id}/reviews/
```json
{
  "text": "string",
  "score": "integer"
}
```

### Получение отзыва по id
GET /api/v1/titles/{title_id}/reviews/{review_id}/

### Добавление комментария к отзыву
POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```json
{
  "text": "string"
}
```

### Регистрация нового пользователя
POST /api/v1/auth/signup/
```json
{
  "email": "string",
  "username": "string"
}
```

### Получение JWT-токена
POST /api/v1/auth/token/
```json
{
  "username": "string",
  "confirmation_code": "string"
}
```

# Articles Platform

Backend-платформа для публикации статей, отзывов и управления пользователями, реализованная на Django + Django REST Framework с базовым frontend и Docker-сборкой.

---

## О проекте

Проект предоставляет API и интерфейс для:

- создания и управления статьями
- добавления отзывов
- регистрации пользователей
- базового отображения страниц через Django templates
- тестирования API
- запуска через Docker

---

## Технологии

- Python 3.12
- Django
- Django REST Framework
- Pytest
- PostgreSQL
- HTML / CSS / JavaScript
- Docker & Docker Compose

---

## Структура проекта
articles/
│
├── articleplatform/
│ ├── article_module/ # статьи
│ ├── reviews/ # отзывы
│ ├── users/ # пользователи
│ ├── templates/ # HTML шаблоны
│ ├── static/ # CSS / JS
│ ├── articleplatform/ # настройки Django
│ ├── manage.py
│ └── pytest.ini
│
├── docker-compose.yml
└── requirements.txt


---

## УСТАНОВКА И ЗАПУСК (LOCAL)

### 1. Клонирование репозитория

```bash
git clone https://github.com/ValeriaKhomutova/articles.git
cd articles
```

```bash
python -m venv venv
venv\Scripts\activate
```


```bash
pip install -r requirements.txt
```

```bash
cd articleplatform
```

```bash
python manage.py makemigrations
python manage.py migrate
```

# Аттестационный API проект

![Python](https://img.shields.io/badge/Python-3.12-blue)  
![Django](https://img.shields.io/badge/Django-5.2.1-brightgreen)  
![DRF](https://img.shields.io/badge/DRF-3.16-red)  
![Coverage](https://img.shields.io/badge/Coverage-86%25-green)  
![GitHub](https://img.shields.io/badge/Repo-GitHub-black)  

---

API для управления иерархической сетью поставщиков с системой контроля продуктов и контактов.

---

## 🌟 Особенности проекта

- Полноценный CRUD для звеньев сети (Завод / Розничная сеть / ИП)
- Кастомная модель пользователя с email-авторизацией
- JWT-аутентификация с refresh-токенами
- Автоматическое определение уровня в иерархии
- Интеграция с Celery для асинхронных задач
- Документированное API (Swagger / Redoc)
- Блокировка пользователя который не входил в сеть больше 45 дней (разблокировка через админку)

---

## 🛠 Технологический стек

| Компонент             | Технология                          |
|-----------------------|-------------------------------------|
| Backend               | Django 5.2.1 + DRF 3.16            |
| База данных           | PostgreSQL 15                     |
| Аутентификация        | JWT (SimpleJWT)                     |
| Документация          | drf-yasg                          |
| Асинхронные задачи    | Celery + Redis                     |
| Тестирование         | pytest (86% покрытие)               |

---

## ⚙️ Быстрый старт

```bash
# Клонирование репозитория
git clone https://github.com/AlPogorelov/CertificationProject.git
cd CertificationProject

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt

# Настройка файла окружения
cp .env.example .env
nano .env  # Заполните параметры конфигурации
```

---

## 📝 Конфигурация файла `.env`

### Обязательные параметры

```
SECRET_KEY=your-secret-key
POSTGRES_DB=supplier_network
POSTGRES_USER=supplier_user
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Для Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

---

## 🚀 Инициализация базы данных

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

После запуска сервера API будет доступен по адресу: `http://localhost:8000/`

---

## 🌐 API Endpoints

### Аутентификация

| Метод | Endpoint                      | Описание                                |
|---------|------------------------------|-----------------------------------------|
| POST    | /api/token/                   | Получение JWT токена                    |
| POST    | /api/token/refresh/           | Обновление токена                      |

### Фильтрация контактов и поставщиков

- **По стране контакта:** `?country=Russia`
- **По уровню поставщика:** `?level=0` (завод), `?level=1` (розница), `?level=2` (ИП)

---

## 📚 Документация API

Доступна после запуска сервера:

- **Swagger UI:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **ReDoc:** [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## 🧪 Тестирование и покрытие

```bash
# Запуск тестов
python manage.py test .

# Генерация отчета покрытия
coverage html
open htmlcov/index.html
```

---

## 🏗 Структура проекта

```
CertificationProject/
├── config/               # Основные настройки проекта
├── network/              # Модуль сети поставщиков
│   ├── models/           # Модели данных
│   ├── api/              # API эндпоинты
│   └── tests/            # Тесты (86% покрытие)
├── users/                # Модуль аутентификации
├── .env.example          # Шаблон файла окружения
└── requirements.txt      # Зависимости
```

---

## Контакты

- **Александр Погорелов** — [eczempl@gmail.com](mailto:eczempl@gmail.com)  
- **GitHub профиль:** [https://github.com/AlPogorelov](https://github.com/AlPogorelov)  
- **Репозиторий проекта:** [https://github.com/AlPogorelov/CertificationProject](https://github.com/AlPogorelov/CertificationProject)

---

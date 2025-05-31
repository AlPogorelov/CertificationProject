import os
from celery import Celery
from celery.schedules import crontab

from config import settings

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('config')

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()

app.conf.timezone = 'UTC'
app.conf.enable_utc = True

app.conf.beat_schedule = {
    'check-inactive-users-daily': {
        'task': 'users.tasks.check_inactive_users',
        'schedule': crontab(hour=3, minute=0),  # Ежедневно в 03:00 UTC
        'args': (45,)  # Дней неактивности
    },
}
from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.db.models import Q
User = get_user_model()


@shared_task
def check_inactive_users(inactive_days=30):
    """
    Блокировка пользователей, не заходивших более указанных дней
    """
    try:
        cutoff_date = timezone.now() - timedelta(days=inactive_days)

        inactive_users = User.objects.filter(
            Q(last_login__lt=cutoff_date) |
            Q(last_login__isnull=True, date_joined__lt=cutoff_date),
            is_active=True
        )

        count = inactive_users.update(is_active=False)

        return f"Успешно заблокировано {count} пользователей"

    except Exception:

        raise

from celery import Task
from celery.utils.log import get_task_logger
from django.utils import timezone
from datetime import timedelta
from .models import User

logger = get_task_logger(__name__)


class DeleteInactiveUsersTask(Task):
    def run(self, *args, **kwargs):
        threshold_date = timezone.now() - timedelta(days=3)
        inactive_users = User.objects.filter(
            is_active=False, date_joined__lt=threshold_date, is_deleted=False
        )
        for user in inactive_users:
            user.delete_logical()
            logger.info(f"User {user.id} deleted logically.")


# Register the task
delete_inactive_users_task = DeleteInactiveUsersTask()

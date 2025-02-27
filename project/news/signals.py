from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from news.models import PostCategory
from news.tasks import create_new_task


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        create_new_task.delay(instance.pk)

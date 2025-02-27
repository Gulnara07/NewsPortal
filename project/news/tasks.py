from datetime import datetime
from celery import shared_task
from celery.schedules import crontab
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post, Category
from project import settings

@shared_task
def weekly_send_email_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_in__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'flatpages/daily_post.html',
    {
        'link' : settings.SITE_URL,
        'posts' : posts
    }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers

    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
def create_new_task(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    title=post.title
    subscribers_emails=[]
    for category in categories:
        subscribers_users = category.subscribers.all()
        for sub_user in subscribers_users:
            subscribers_emails.append(sub_user.email)

    html_content = render_to_string(
        'flatpages/post_created_email.html',
        {
            'link': f'{settings.SITE_URL}/news/{pk}',
            'text': f'{post.title}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails

    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()



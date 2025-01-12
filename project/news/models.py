from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.core.validators import MinValueValidator
from django.urls import reverse

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comments_rating = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        posts_comments_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum('rating'), 0))['pcr']


        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()
    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name.title()

class Post(models.Model):

    news = 'NW'
    articles = 'AR'

    POST_TYPES = [
        (news, 'Новость'),
        (articles, 'Статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=articles)
    date_in = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()
        return self.rating

    def dislike(self):
        self.rating -= 1
        self.save()
        return self.rating

    def preview(self):
        if len(self.text) > 124:
            return f'{self.text[:124]} ...'
        else:
            return f'{self.text[:len(self.text)]}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default="Без содержания")
    date_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating +=1
        self.save()
        return self.rating

    def dislike(self):
        self.rating -=1
        self.save()
        return self.rating

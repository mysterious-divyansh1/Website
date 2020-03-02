from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='avatar_images', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bookmarks = models.ManyToManyField('Article')

    def __str__(self):
        return self.user.username


class Article(models.Model):
    title = models.CharField(max_length=100)
    published = models.CharField(max_length=100)
    summary = models.CharField(max_length=300)
    link = models.CharField(max_length=100)

    def __str__(self):
        return self.link

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings


class User(AbstractUser):
  pass

class Category(models.Model):
  name = models.CharField(max_length=100)
  slug = models.SlugField(null=True, unique=True, max_length=250)

  def __str__(self):
    return self.name

  class Meta:
    ordering = ('name',)
    verbose_name = 'category'
    verbose_name_plural = 'categories'

class Post(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
  category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
  title = models.CharField(max_length=100)
  content = models.TextField()
  image = models.ImageField(default='default.jpg')
  date_posted = models.DateTimeField(default=timezone.now)
  slug = models.SlugField(null=True, unique=True, max_length=250)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
      return reverse('blog-post-view', kwargs={'slug': self.slug})

class Comment(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  reply = models.ForeignKey('Comment', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
  content = models.TextField()
  date_posted = models.DateTimeField(default=timezone.now)

  def __str__(self):
      return self.content

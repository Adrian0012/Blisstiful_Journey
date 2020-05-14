from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings


class User(AbstractUser):
  pass

class Post(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField()
  date_posted = models.DateTimeField(default=timezone.now)
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
  #you can check for more on_delete options

  def __str__(self):
    return self.title

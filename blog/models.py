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
  image = models.ImageField(default='default.jpg')
  slug = models.SlugField(null=True, unique=True)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
      return reverse('blog-post-view', kwargs={'slug': self.slug})

class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
  content = models.TextField()
  date_posted = models.DateTimeField(default=timezone.now)
  approved_comment = models.BooleanField(default=False)

  def approve(self):
      self.approved_comment = True
      self.save()

  def __str__(self):
      return self.content

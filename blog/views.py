from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required

def index(request):
  data = {
    'posts' : Post.objects.all()
  }
  return render(request, 'bliss_blog/index.html', data)


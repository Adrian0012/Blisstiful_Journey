from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required

def index(request):
  data = {
    'posts' : Post.objects.all()
  }
  return render(request, 'blog/index.html', data)

def about(request):
  return render(request, 'blog/about.html')

def contact(request):
  return render(request, 'blog/contact.html')

@login_required
def view_post(request, pk):
  post = Post.objects.get(pk=pk)
  return render(request, 'blog/post.html', {'post' : post})
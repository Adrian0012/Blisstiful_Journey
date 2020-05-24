from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages

#Index page
def index(request):
  data = {
    'posts' : Post.objects.all()
  }
  return render(request, 'blog/index.html', data)

#Contact page
def contact(request):
  if request.method == 'POST':

    contact_name = request.POST.get('contact-name') 
    contact_email = request.POST.get('contact-email')
    contact_message = request.POST.get('contact-message')

    context = {
      'contact_name': contact_name,
      'contact_email': contact_email,
      'contact_message': contact_message
    }
    send_mail(
      'Personal Message From: ' + contact_name, #subject
      contact_message, #message
      contact_email, #from email
      ['Blisstiful.Journey@gmail.com'] #to email
    )

    messages.success(request, 'Your message has been sent!')
    return render(request, 'blog/contact.html', context)

  else:
    return render(request, 'blog/contact.html')

#About page
def about(request):
  return render(request, 'blog/about.html')

#View Post
@login_required
def view_post(request, slug):
  post = Post.objects.get(slug=slug)
  comments = post.comments.filter(approved_comment=True)

  context = {'post' : post, 'comments' : comments,}

  return render(request, 'blog/post.html', context)

#Create comment for posts
@login_required
def create_comment(request, slug):
  post = Post.objects.get(slug=slug)
  
  if request.method == "POST":
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.author = request.user
      comment.post = post
      comment.save()
      return redirect('blog-post-view', slug=post.slug)
  else:
      form = CommentForm()
  return render(request, 'blog/create_comment.html', {'form': form, 'post' : post})

#Update comments for posts
def update_comment(request):
  pass

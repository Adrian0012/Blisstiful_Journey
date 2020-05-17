from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages

def index(request):
  data = {
    'posts' : Post.objects.all()
  }
  return render(request, 'blog/index.html', data)

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

def about(request):
  return render(request, 'blog/about.html')

@login_required
def view_post(request, pk):
  post = Post.objects.get(pk=pk)
  return render(request, 'blog/post.html', {'post' : post})
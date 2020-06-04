from django.shortcuts import render, redirect
from .models import Post, Comment, Category
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse

#Index page
def index(request):
  data = {
    'posts' : Post.objects.all(),
    'categories' : Category.objects.all()
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
  comments = post.comments.filter(approved_comment=True, reply=None).order_by('-date_posted')

  if request.method == "POST":
    form = CommentForm(request.POST)
    if form.is_valid():
      content = request.POST.get('content')
      print(content)
      reply_id = request.POST.get('comment_id')
      data = None
      if reply_id:
        data = Comment.objects.get(id=reply_id)

      comment = Comment.objects.create(post=post, user=request.user, content=content, reply=data)
      comment.save()
    else:
      print (form.errors)

  else:
    form = CommentForm()

  context = {
    'post' : post,
    'comments' : comments,
    'form' : form
  }

  if request.is_ajax():
    html = render_to_string('blog/comments.html', context, request=request)
    return JsonResponse({ 'form' : html })

  return render(request, 'blog/post.html', context)

#Category Detail
@login_required
def view_category(request, slug):
  category = Category.objects.get(slug=slug)
  posts = Post.objects.filter(category=category)

  context = {
    'category' : category,
    'posts' : posts
  }

  return render(request, 'blog/category_view.html', context)

# Create comment for posts
# @login_required
# def create_comment(request, slug):
#   if request.method == "POST":
#     form = CommentForm(request.POST)
#     if form.is_valid():
#       comment = form.save(commit=False)
#       reply_id = request.POST.get('comment_id')
#       data = None

#       if reply_id:
#         data = Comment.objects.get(id=reply_id)
      
#       comment.author = request.user
#       comment.post = post
#       comment.reply = data
#       comment.save()    
#   else:
#       form = CommentForm()

#   context = {
#     'post' : post,
#     'comments' : comments,
#     'form' : form
#   }

#   if request.is_ajax():
#     html = render_to_string('blog/comments.html', context, request=request)
#     return JsonResponse({ 'form' : html })
#   else:  
#     return render(request, 'blog/post.html', context)

#Update comments for posts
def update_comment(request):
  pass

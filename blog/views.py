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
    'posts' : Post.objects.all()[:5],
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
      'contact_message': contact_message,
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
    return render(request, 'blog/contact.html', {'categories' : Category.objects.all()})

#About page
def about(request):
  return render(request, 'blog/about.html', {'categories' : Category.objects.all()})

#View/Comment/Reply Post
@login_required
def view_post(request, slug):
  post = Post.objects.get(slug=slug)
  comments = post.comments.filter(post=post, reply=None).order_by('-date_posted')

  is_liked = False
  if post.likes.filter(id=request.user.id).exists():
    is_liked = True

  if request.method == "POST":
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      reply_id = request.POST.get('comment_id')
      data = None

      if reply_id:
        data = Comment.objects.get(id=reply_id)
      
      comment.author = request.user
      comment.post = post
      comment.reply = data
      comment.save()    
  else:
      form = CommentForm()

  context = {
    'post' : post,
    'comments' : comments,
    'form' : form,
    'is_liked' : is_liked,
    'total_likes' : post.total_likes(),
    'categories' : Category.objects.all()
  }

  if request.is_ajax():
    html = render_to_string('blog/comments.html', context, request=request)
    return JsonResponse({ 'form' : html })
  else:  
    return render(request, 'blog/post.html', context)

#Post Likes
@login_required
def post_like(request, slug):
  post = Post.objects.get(slug=slug)
  is_liked = False

  if post.likes.filter(id=request.user.id).exists():
    post.likes.remove(request.user)
    is_liked = False
  else:
    post.likes.add(request.user)
    is_liked = True

  context = {
    'post' : post,
    'is_liked' : is_liked,
    'total_likes' : post.total_likes()
  }
  if request.is_ajax():
    html = render_to_string('blog/post_likes.html', context, request=request)
    return JsonResponse({ 'form' : html })
    
#Category Detail
def view_category(request, slug):
  category = Category.objects.get(slug=slug)
  posts = Post.objects.filter(category=category).order_by('-date_posted')

  context = {
    'category' : category,
    'posts' : posts,
    'categories' : Category.objects.all()
  }

  return render(request, 'blog/category_view.html', context)

#Update comments for posts
def update_comment(request):
  pass

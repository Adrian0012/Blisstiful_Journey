from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Post, Comment, Category
from taggit.models import Tag
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#Index page
def index(request):
  data = {
    'posts' : Post.objects.all()[:5],
    'categories' : Category.objects.all(),
    'common_tags' : Post.tags.most_common(),

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
      contact_message + '\n\n' + contact_email, #message
      contact_email, #from email
      ['Blisstiful.Journey@gmail.com'] #to email
    )

    messages.success(request, 'Your message has been sent!')
    return render(request, 'blog/contact.html', context)

  else:
    context = {
    'categories' : Category.objects.all(),
    'common_tags' : Post.tags.most_common(),
    }

    return render(request, 'blog/contact.html', context)

#Support page
def support(request):
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
      'Support Ticket From: ' + contact_name, #subject
      contact_message + '\n\n' + contact_email, #message
      contact_email, #from email
      ['Blisstiful.Journey@gmail.com'] #to email
    )

    messages.success(request, 'Your ticket has been sent! We will get back to you shortly.')
    return render(request, 'blog/support.html', context)

  else:
    context = {
    'categories' : Category.objects.all(),
    'common_tags' : Post.tags.most_common(),
    }

    return render(request, 'blog/support.html', context)

#About page
def about(request):
  context = {
    'categories' : Category.objects.all(),
    'common_tags' : Post.tags.most_common(),
  }

  return render(request, 'blog/about.html', context)

def privacy_and_policy(request):
  context = {
  'categories' : Category.objects.all(),
  'common_tags' : Post.tags.most_common(),
  }

  return render(request, 'blog/privacy_and_policy.html', context)

#View/Comment/Reply Post
def view_post(request, slug):
  post = Post.objects.get(slug=slug)
  comments = post.comments.filter(post=post, reply=None).order_by('-date_posted')
  common_tags = Post.tags.most_common()
  
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
      form.save_m2m()    
  else:
      form = CommentForm()

  context = {
    'post' : post,
    'comments' : comments,
    'form' : form,
    'is_liked' : is_liked,
    'total_likes' : post.total_likes(),
    'categories' : Category.objects.all(),
    'common_tags' : common_tags
  }

  if request.is_ajax():
    html = render_to_string('blog/comments.html', context, request=request)
    return JsonResponse({ 'form' : html })
  else:  
    return render(request, 'blog/post.html', context)

#Category View Detail
def view_category(request, slug):
  category = Category.objects.get(slug=slug)
  posts = Post.objects.filter(category=category).order_by('-date_posted')
  paginator = Paginator(posts, 2)
  page = request.GET.get('page')

  try:
      posts = paginator.page(page)
  except PageNotAnInteger:
      posts = paginator.page(1)
  except EmptyPage:
      posts = paginator.page(paginator.num_pages)

  context = {
    'category' : category,
    'posts' : posts,
    'paginator' : paginator,
    'categories' : Category.objects.all(),
    'common_tags' : Post.tags.most_common(),
  }

  return render(request, 'blog/category_view.html', context)

def tagged(request, slug):
  tag = Tag.objects.get(slug=slug)
  posts = Post.objects.filter(tags=tag)
  paginator = Paginator(posts, 5)
  page = request.GET.get('page')

  try:
      posts = paginator.page(page)
  except PageNotAnInteger:
      posts = paginator.page(1)
  except EmptyPage:
      posts = paginator.page(paginator.num_pages)


  context = {
    'tag' : tag,
    'posts' : posts,
    'categories' : Category.objects.all(),
    'paginator' : paginator,
  }

  return render(request, 'blog/tag_view.html', context)
  
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
    

#Update comments for posts
def update_comment(request):
  pass

#Update replies for posts
def update_replies(request):
  pass

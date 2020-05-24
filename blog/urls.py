from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog-index'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    path('post/<int:pk>/', views.view_post, name='blog-post-view'),
    path('post/<int:pk>/comment', views.create_comment, name='blog-comment'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog-index'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    path('support/', views.support, name='blog-support'),
    path('privacy-and-policy/', views.privacy_and_policy, name='blog-privacy-and-policy'),
    path('post/<slug:slug>/', views.view_post, name='blog-post-view'),
    path('post/<slug:slug>/like/', views.post_like, name='blog-post-like'),
    path('category-detail/<slug:slug>/', views.view_category, name='view-category'),
    path('tags/<slug:slug>/', views.tagged, name='view-tag')
]
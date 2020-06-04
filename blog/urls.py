from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog-index'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    path('post/<slug:slug>/', views.view_post, name='blog-post-view'),
    # path('post/<slug:slug>/comment/', views.create_comment, name='blog-comment'),
    path('category-detail/<slug:slug>/', views.view_category, name='view-category')
]
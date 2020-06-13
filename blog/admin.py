from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Comment, Category

admin.site.site_header = 'Blisstiful Journey'
admin.site.site_title = 'Blisstiful Journey'
admin.site.index_title = 'Blisstiful Journey'

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name',)
  list_filter = ('name',)
  search_fields = ('name', 'content')
  prepopulated_fields = {"slug": ("name",)}

class PostAdmin(admin.ModelAdmin):
  date_hierarchy = 'date_posted'
  list_display = ('title', 'author', 'date_posted', 'tag_list')
  list_filter = ('date_posted','author')
  search_fields = ('title', 'content')
  prepopulated_fields = {"slug": ("title",)}
  #excluding datetime field from form
  exclude = ('date_posted',)

  def get_queryset(self, request):
    return super().get_queryset(request).prefetch_related('tags')

  def tag_list(self, obj):
    return u", ".join(o.name for o in obj.tags.all())

  fieldsets = [
    (None, {'fields' : ['author']}),
    ('Select a Category', {'fields' : ['category']}),
    ('Write your post', {'fields' : ['title', 'content']}),
    ('Tags', {'fields' : ['tags']}),
    ('Upload Image', {'fields' : ['image']}),
    ('Slug', {'fields' : ['slug']}),
  ]

class CommentAdmin(admin.ModelAdmin):
  date_hierarchy = 'date_posted'
  list_display = ('content', 'author')
  list_filter = ('date_posted', 'author')
  search_fields = ('content', 'content')

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)



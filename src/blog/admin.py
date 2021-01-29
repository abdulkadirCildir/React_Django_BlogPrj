from django.contrib import admin
import nested_admin
from .models import Category, Post, Comment, Like, PostView

class PostViewInline(nested_admin.NestedTabularInline):
    model = PostView
    
class LikeInline(nested_admin.NestedTabularInline):
    model = Like

class CommentInline(nested_admin.NestedTabularInline):
    model = Comment

class PostInline(nested_admin.NestedTabularInline):
    model = Post
    inlines = [CommentInline, LikeInline, PostViewInline]

class BlogAdmin(nested_admin.NestedModelAdmin):
    model = Category
    inlines = [PostInline]

admin.site.register(Category, BlogAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(PostView)
# Register your models here.

"""admin.py"""
from django.contrib import admin
from blogapp.models import Post, Comment, Tag, Profile


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Profile)

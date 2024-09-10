from django.contrib import admin
from .models import Tag, Post
# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)

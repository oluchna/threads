from django.contrib import admin
from .models import Tag, Post, Profile
# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Profile)

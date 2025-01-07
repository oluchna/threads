from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Tag, Post, Profile
# Register your models here.

class PostAdmin(SummernoteModelAdmin):  
    summernote_fields = ('content',)

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Profile)


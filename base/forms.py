from django.forms import ModelForm, ModelMultipleChoiceField
from .models import Post, Tag


class ThreadForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
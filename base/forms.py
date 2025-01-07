from django.forms import ModelForm, ModelMultipleChoiceField
from .models import Post, Tag
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class ThreadForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tag']

        widgets = {
            'content': SummernoteWidget(),  
        }
        

    tag = ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    def save(self, commit=True):
        post = super().save(commit=False)
        
        if commit:
            post.save()
        
        tag = self.cleaned_data.get('tag')
        if tag:
            post.tag.set(tag, through_defaults={'database': 'default'})  # Associate selected tags with the post
            
        return post
from django.forms import ModelForm, ModelMultipleChoiceField
from .models import Post, Tag


class ThreadForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tag']

    tag = ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    def save(self, commit=True):
        # Save the post first to get a Post instance
        post = super().save(commit=False)
        
        # Save the Post instance, but don't commit yet
        if commit:
            post.save()
        
        # Save the tags relationship
        tag = self.cleaned_data.get('tag')
        if tag:
            post.tag.set(tag, through_defaults={'database': 'default'})  # Associate selected tags with the post
            
        return post
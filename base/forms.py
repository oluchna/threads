from django.forms import ModelForm, ModelMultipleChoiceField, SelectMultiple, TextInput
from .models import Post, Tag
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class ThreadForm(ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tag']

        widgets = {
            'title': TextInput(attrs={
                'class': 'create-thread-title', 
                'placeholder': 'Title'}),
            'content': SummernoteWidget(attrs={
                'class': 'thread-input',
                'width': '100%',
            }),
        }
        

    tag = ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False,  widget=SelectMultiple(attrs={
            'class': 'form-control-tags',
        }))

    def save(self, commit=True):
        post = super().save(commit=False)
        
        if commit:
            post.save()
        
        tag = self.cleaned_data.get('tag')
        if tag:
            post.tag.set(tag, through_defaults={'database': 'default'})  # Associate selected tags with the post
            
        return post

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         if field.required:
    #             # Append the asterisk to the placeholder
    #             placeholder = field.widget.attrs.get('placeholder', field.label)
    #             field.widget.attrs['placeholder'] = f"{placeholder}*"
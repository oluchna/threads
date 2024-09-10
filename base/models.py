from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Tag(models.Model):

    class TagType(models.TextChoices):
        TECHNOLOGY = 'TECH', 'Technology'
        EDUCATION = 'EDU', 'Education'
        ENTERTAINMENT = 'ENT', 'Entertainment'
        HEALTH = 'HEA', 'Health'
        LIFESTYLE = 'LIFE', 'Lifestyle'

    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    name = models.CharField(
        max_length=50,
        choices=TagType.choices,
        default=TagType.LIFESTYLE,
        unique=True
    )

    def __str__(self):
        return self.get_name_display()
 

# class User(models.Model):
#     user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     username = models.CharField(max_length=100, null=True)



class Post(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    title = models.CharField(max_length=300, null=False, blank=False)

    POST_TYPE = (
        ('t', 'Thread'), 
        ('p', 'Post'), 
        ('c', "Comment")
    )
    post_type = models.CharField(max_length=1, choices=POST_TYPE, blank=False)
    parent_type = models.CharField(max_length=1, choices=POST_TYPE, blank=True)
    
    parent_post = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='child_posts')
    
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    tag = models.ManyToManyField(Tag)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title
    
    # def clean(self):
    #     # Rule 1: If post_type is 't', parent_type and parent_post must be null
    #     if self.post_type == 't':
    #         if self.parent_type is not None or self.parent_post is not None:
    #             raise ValidationError({
    #                 'parent_type': 'A thread (post_type="t") cannot have a parent_type.',
    #                 'parent_post': 'A thread (post_type="t") cannot have a parent_post.'
    #             })
    #         self.parent_type = None
    #         self.parent_post = None

    #     # Rule 2: If post_type is 'p', parent_type must be 't', and parent_post must be set
    #     elif self.post_type == 'p':
    #         if self.parent_type != 't':
    #             raise ValidationError({
    #                 'parent_type': 'A post (post_type="p") must have parent_type set to "t".'
    #             })
    #         if not self.parent_post:
    #             raise ValidationError({
    #                 'parent_post': 'A post (post_type="p") must have a parent_post selected.'
    #             })

    # def save(self, *args, **kwargs):
    #     # Call clean to ensure the validation rules are enforced before saving
    #     self.clean()
    #     super().save(*args, **kwargs)


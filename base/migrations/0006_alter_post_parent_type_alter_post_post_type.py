# Generated by Django 5.1 on 2024-09-03 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_rename_post_author_post_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='parent_type',
            field=models.CharField(blank=True, choices=[('t', 'Thread'), ('p', 'Post'), ('c', 'Comment')], max_length=1),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('t', 'Thread'), ('p', 'Post'), ('c', 'Comment')], max_length=1),
        ),
    ]

# Generated by Django 4.0.4 on 2022-06-20 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_status_alter_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.DateTimeField(blank=True, help_text='The date and time this article was published', null=True),
        ),
    ]

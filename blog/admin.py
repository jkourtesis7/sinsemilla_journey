"""blog/admin.py"""

from django.contrib import admin
from blog.models import Post, Comment
from . import models


# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    """Comment Admin"""

    list_display = (
        'name',
        'email',
        'text',
        'approved',
    )

    search_fields = (
        'post',
        'name',
        'email',
        'text',
    )

    list_filter = (
        'approved',
    )


admin.site.register(models.Comment, CommentAdmin)

class CommentInline(admin.StackedInline):
    """create inline"""
    model = Comment

    readonly_fields = (
        'name',
        'text',
        'email',
    )

class PostAdmin(admin.ModelAdmin):
    """Post Admin"""
    inlines = [CommentInline,]

    prepopulated_fields = {'slug':('title',)}

    list_display = (
        'title',
        'author',
        'created',
        'updated',
    )

    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )

    list_filter = (
        'status',
        'topics',
    )

admin.site.register(models.Post, PostAdmin)

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    """Topic Admin"""
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug':('name',)}

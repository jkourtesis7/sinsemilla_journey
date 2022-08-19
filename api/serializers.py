from rest_framework import serializers
from blog.models import Post, Comment

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'author',
            'published',
        ]

class PostDetailSerializer(serializers.ModelSerializer):
    # Get the full name of the Author
    author_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'author',
            'author_full_name',
            'banner',
            'content',
            'published',
        ]

    def get_author_full_name(self, obj):
        """
        Returns the authors full name
        """
        return obj.author.get_full_name()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'name',
            'email',
            'text',
            'created',
            'likes',
            'dislikes',
        ]

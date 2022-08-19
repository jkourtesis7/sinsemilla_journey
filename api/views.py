""" api/views.py """

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.models import Post, Comment
from . import serializers
from django.db.models import F

# Expose a view to the root of the API using a function for API index
@api_view(['GET'])
def index(request):
    """ api view """
    return Response()

class PostListView(generics.ListAPIView):
    """
    Returns a list of published Posts
    """
    serializer_class = serializers.PostListSerializer
    queryset = Post.objects.published()

class PostDetailView(generics.RetrieveAPIView):
    """
    Returns post Post Details
    """
    serializer_class = serializers.PostDetailSerializer
    queryset = Post.objects.published()

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        post_id = self.request.query_params.get('post')
        queryset = super().get_queryset()
        if post_id and post_id.isdecimal():
            queryset = queryset.filter(post_id=int(post_id))

        return queryset.order_by('-created')

def CommentLikeView(request, pk):
    queryset = Comment.objects.get(pk=pk)
    queryset.likes = F('likes') + 1
    queryset.save()
    queryset.refresh_from_db()

def CommentDislikeView(request, pk):
    queryset = Comment.objects.get(pk=pk)
    queryset.dislikes = F('dislikes') + 1
    queryset.save()
    queryset.refresh_from_db()

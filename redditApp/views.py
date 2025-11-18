from .serializer import PostSerializer, CommentSerializer
from .models import Posts, Comments
from rest_framework import viewsets

class PostViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all().prefetch_related('comments')
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
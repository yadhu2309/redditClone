from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField
from .models import Posts, Comments

class RecursiveField(Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CommentSerializer(ModelSerializer):
    replies = RecursiveField(many=True, read_only=True) 
    class Meta:
        model = Comments
        fields = '__all__'

class PostSerializer(ModelSerializer):
    comments = SerializerMethodField()
    class Meta:
        model = Posts
        fields = '__all__'

    def get_comments(self, obj):
        # return only top-level comments (parent = None)
        top_level_comments = obj.comments.filter(comment__isnull=True)
        return CommentSerializer(top_level_comments, many=True).data

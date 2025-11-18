from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField
from .models import Posts, Comments

class RecursiveField(Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CommentSerializer(ModelSerializer):
    replies = SerializerMethodField()
    class Meta:
        model = Comments
        fields = '__all__'
    def get_replies(self, obj):
        return CommentSerializer(obj.get_children(), many=True).data

class PostSerializer(ModelSerializer):
    comments =CommentSerializer()
    class Meta:
        model = Posts
        fields = '__all__'
    def get_comments(self, obj):
        return CommentSerializer(obj.comments.filter(parent__isNull=True), many=True).data

    # def get_comments(self, obj):
    #     # return only top-level comments (parent = None)
    #     top_level_comments = obj.comments.filter(comment__isnull=True)
    #     return CommentSerializer(top_level_comments, many=True).data

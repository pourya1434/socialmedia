from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.abstract.serializers import AbstractSerializer
from core.user.serializers import UserSerializer

from core.user.models import User
from core.post.models import Post
from core.comment.models import Comment




class CommentSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='public_id')
    post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='public_id')

    def validate_post(self, value):
        if self.instance:
            return self.instance.post
        return value
    
    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True
        instance = super().update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(rep["author"])
        rep['author'] = UserSerializer(author).data

        return rep
    

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'body', 'edited', 'created', 'updated']

        read_only_fields = ["edited"]
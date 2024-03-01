from rest_framework import serializers
from ..models import Post, Like
from users.api.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = "__all__"

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Like
        fields = '__all__'
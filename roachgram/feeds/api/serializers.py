from rest_framework import serializers
from ..models import Post, Like , Media
from users.api.serializers import UserSerializer

class GetMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ["file"]

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    media_url = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = "__all__"


    def get_media_url(self , obj):
        try:
            media = Media.objects.filter(post=obj)
        except Media.DoesNotExist:
            return None

        serializer = GetMediaSerializer(media , many=True)

        return serializer.data
        


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class SaveMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"

class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Like
        fields = '__all__'
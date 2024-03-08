from rest_framework import serializers
from ..models import Post, Like , Media , Comment
from users.api.serializers import UserSerializer

class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = ["id","file"]

    def create(self, validated_data , postInstance):
        files = validated_data.pop("file")
        for file in files:
            Media.objects.create(post=postInstance , file=file)

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = "__all__"



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

        serializer = MediaSerializer(media , many=True)

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
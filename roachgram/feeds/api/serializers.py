from rest_framework import serializers
from ..models import Post, Like , Media , Comment , Bookmark
from users.api.serializers import UserSerializer
from django.utils.html import escape

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

    def validate_caption(self , value):
        return escape(value)


class DynamicPostSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class PostSerializer(DynamicPostSerializer):
    user = UserSerializer(read_only=True , fields=["id" , "name" , "username" , "profile"])
    media_url = serializers.SerializerMethodField()
    # a boolean field for knowing if logged in user liked post or not
    liked = serializers.SerializerMethodField(method_name="liked_before")
    likesCount = serializers.SerializerMethodField(method_name="likes_count")
    commentsCount = serializers.SerializerMethodField(method_name="comments_count")
    # another boolean field for knowing if logged in user bookmarked post or not
    bookmarked = serializers.SerializerMethodField(method_name="bookmarked_before")
    bookmarksCount = serializers.SerializerMethodField(method_name="bookmarks_count")
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

    def liked_before(self , obj):
        # the context is from calling serializer in viewsets
        request = self.context.get("request" , None)
        
        liked = False

        try:
            Like.objects.get(post=obj , user=request.user.id)
            liked = True
        except Like.DoesNotExist:
            pass


        return liked
    
    def bookmarked_before(self , obj):
        # the context is from calling serializer in viewsets
        request = self.context.get("request" , None)
        bookmarked = False
        try:
            Bookmark.objects.get(user=request.user.id , post=obj)
            bookmarked = True
        except Bookmark.DoesNotExist:
            pass

        return bookmarked
    

    def likes_count(self , obj):
        return Like.objects.filter(post=obj.id).count()
    
    def comments_count(self , obj):
        return Comment.objects.filter(repliedTo=obj).count()
    
    def bookmarks_count(self , obj):
        return Bookmark.objects.filter(post=obj).count()


   
class GetCommentSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only=True, fields=["id" , "name" , "username" , "profile"])
    repliedTo = PostSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def validate_caption(self , value):
        return escape(value)

class SaveMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"

class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Like
        fields = '__all__'


class CreateBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = "__all__"

class BookmarkSerializer(CreateBookmarkSerializer):
    post = PostSerializer(read_only=True)
from rest_framework import serializers
from ..models import User , FollowUser
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser , FormParser , JSONParser , FileUploadParser


class DynamicUserSerializer(serializers.ModelSerializer):
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

class UserSerializer(DynamicUserSerializer):
    isFollowing = serializers.SerializerMethodField(method_name="is_following_user")
    followersCount = serializers.SerializerMethodField(method_name="followers_count")
    followingsCount = serializers.SerializerMethodField(method_name="followings_count")
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "username",
            "isFollowing",
            "followersCount",
            "followingsCount",
            "about",
            "profile",
            "date_joined"
        ]

    def is_following_user(self , obj):
        isFollowing = False
        request = self.context.get("request")
        try:
            FollowUser.objects.get(follower=request.user.id , following=obj)
            isFollowing = True
        except FollowUser.DoesNotExist:
            pass

        return isFollowing
    
    def followers_count(self , obj):
        return FollowUser.objects.filter(following=obj).count()
    
    def followings_count(self , obj):
        return FollowUser.objects.filter(follower=obj).count()
    

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name" , "username" , "about" , "password" , "email" , "profile"]



    
class UpdateUserSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username" , "name" , "email" , "profile" , "about"]


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUser
        fields = "__all__"

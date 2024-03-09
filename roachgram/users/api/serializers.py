from rest_framework import serializers
from ..models import User , FollowUser
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser , FormParser , JSONParser , FileUploadParser

class UserSerializer(serializers.ModelSerializer):
    isFollowing = serializers.SerializerMethodField(method_name="is_following_user")

    class Meta:
        model = User
        fields = ["id" , "name" , "username" , "isFollowing" , "about" , "profile" , "date_joined"]

    def is_following_user(self , obj):
        isFollowing = False
        request = self.context.get("request")
        try:
            FollowUser.objects.get(follower=request.user.id)
            isFollowing = True
        except FollowUser.DoesNotExist:
            pass

        return isFollowing
    

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

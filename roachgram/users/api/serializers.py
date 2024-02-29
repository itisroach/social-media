from rest_framework import serializers
from ..models import User

class CreateUserSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name" , "username" , "about" , "password" , "email" , "profile"]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class UpdateUserSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username" , "name" , "email" , "profile" , "about"]


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
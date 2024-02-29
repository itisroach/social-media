from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import CreateUserSeralizer , UpdateUserSeralizer , ChangePasswordSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from ..models import User
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

class MyTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)


        token['name']     = user.name
        token['username'] = user.username
        token["profile"]  = user.profile.url
        token["about"]    = user.about

        return token
    
class MyToken(TokenObtainPairView):
    serializer_class = MyTokenSerializer


@api_view(["POST"])
def createUser(request):
    serializer = CreateUserSeralizer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.create(request.data)
    return Response(serializer.data)


class UpdateUser(UpdateAPIView):
    serializer_class = UpdateUserSeralizer
    permission_classes = [IsAuthenticated,]
    lookup_field = "pk"
    
    

    def get_queryset(self):
        return self.request.user


    def update(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance , data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ChangePassword(UpdateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        old_pass = request.data.get("old_password")
        new_pass = request.data.get("new_password")

        if serializer.is_valid():
            if not user.check_password(old_pass):
              return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_pass)
            user.save()
            return Response({'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully'})
          
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
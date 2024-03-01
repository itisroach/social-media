from rest_framework.views import APIView
from .serializers import PostSerializer , CreatePostSerializer
from ..models import Post
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied , NotAuthenticated
from rest_framework.generics import RetrieveAPIView

class PostViews(APIView):

    def get(self , request , format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts , many=True)
        return Response(serializer.data)


    def post(self , request , format=None):
        
        if request.user.is_authenticated:
            if request.user.id != request.data["user"]:
                raise PermissionDenied
        
            serializer = CreatePostSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        else:
            raise NotAuthenticated
    
    def delete(self, request , format=None):
        if request.user.is_authenticated:
            try:
                post = Post.objects.get(id=request.data["id"])
            except Post.DoesNotExist:
                return Response({"message":"post not found"} , status=status.HTTP_404_NOT_FOUND)
            if post.user.id != request.user.id:
                raise PermissionDenied
            
            post.delete()

            return Response({"message":"post deleted successfully"} , status=status.HTTP_200_OK)
        else:
            raise NotAuthenticated
        

class PostDetailView(RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
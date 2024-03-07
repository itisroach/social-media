from rest_framework.views import APIView
from .serializers import (
    PostSerializer , 
    CreatePostSerializer , 
    LikePostSerializer,
    SaveMediaSerializer,
    CommentSerializer,
    )


from ..models import Post , Like , Comment
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied , NotAuthenticated
from rest_framework.views import Http404
from rest_framework.generics import RetrieveAPIView , ListAPIView

class PostViews(APIView):
    def get(self , request , format=None):
        posts = Post.objects.filter(isReply=False).order_by('-createdAt')
        serializer = PostSerializer(posts , many=True)
        return Response(serializer.data)


    def post(self , request , format=None):
        
        if request.user.is_authenticated:
            if request.user.id != int(request.data["user"]):
                raise PermissionDenied
        
        
            serializer = CreatePostSerializer(data=request.data)

            if serializer.is_valid():
                post = serializer.save()
                
                # uploading files
                if request.FILES:
                    request.data["post"] = post.id
                    mediaSerializer = SaveMediaSerializer(data=request.data)
                    if mediaSerializer.is_valid():
                        mediaSerializer.save()
                        postSerializer = PostSerializer(post)
                        return Response(postSerializer.data , status=status.HTTP_201_CREATED)
                    else:
                        return Response(post.errors , status=status.HTTP_400_BAD_REQUEST)
                    
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


class CommentView(APIView):
    def get(self, request, pk , format=None):


        comments = Comment.objects.filter(repliedTo=pk)

        if len(comments) < 1:
            raise Http404

        serializer = PostSerializer(comments , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    

    def post(self , request , pk , format=None):
        if request.user.is_authenticated:
            if request.user.id != int(request.data["user"]):
                raise PermissionDenied


    
            request.data["repliedTo"] = int(pk)
            request.data["isReply"] = True
         
            serializer = CommentSerializer(data=request.data)

            if serializer.is_valid():
                comment = serializer.save()

                commentSerializer = PostSerializer(comment)

                if request.FILES:
                 
                    request.data["post"] = comment.id
               
                    mediaSerializer = SaveMediaSerializer(data=request.data)
                    
                    if mediaSerializer.is_valid():
                        mediaSerializer.save()
                        return Response(commentSerializer.data , status=status.HTTP_201_CREATED)

                    return Response(mediaSerializer.errors , status=status.HTTP_400_BAD_REQUEST)
                
                return Response(commentSerializer.data , status=status.HTTP_201_CREATED)
            
            # bad request 
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

        else:
            raise NotAuthenticated
        

    def delete(self , request, pk , format=None):
        if request.user.is_authenticated:
            try:
                comment = Comment.objects.get(id=request.data["id"])
            except Comment.DoesNotExist:
                return Response({"message":"comment not found"} , status=status.HTTP_404_NOT_FOUND)
            if comment.user.id != request.user.id:
                raise PermissionDenied
            
            comment.delete()

            return Response({"message":"comment deleted successfully"} , status=status.HTTP_200_OK)
        else:
            raise NotAuthenticated


class UserPostListView(ListAPIView):
    serializer_class = PostSerializer
    lookup_field = "username"

    def get_queryset(self):
        posts = Post.objects.filter(user__username=self.kwargs["username"]).order_by('-createdAt')
        serializer = self.get_serializer(posts , many=True)
        return serializer.data
    

class LikePostView(APIView):
    
    def post(self , request , format=None):
        
        likeInstance = Like.objects.filter(user=request.user.id , post=request.data["post"])

        if likeInstance.exists():
            return Response({"message": "post liked before"} , status=status.HTTP_409_CONFLICT)

        if request.user.is_authenticated:
            request.data["user"] = request.user.id
            serializer = LikePostSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "liked post"} , status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

        else:
            raise NotAuthenticated
        

    def delete(self , request , format=None):
        
        if request.user.is_authenticated:
            request.data["user"] = request.user.id
            try:
                likeInstance = Like.objects.get(post=request.data["post"] , user=request.data["user"])
            except Like.DoesNotExist:
                raise Http404
            
            likeInstance.delete()

            return Response({"message": "successfully removed from your likes"} , status=status.HTTP_200_OK)
        else:
            raise NotAuthenticated
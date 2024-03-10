from rest_framework.views import APIView
from .serializers import (
    PostSerializer , 
    CreatePostSerializer , 
    LikePostSerializer,
    CommentSerializer,
    MediaSerializer,
    CreateBookmarkSerializer,
    BookmarkSerializer
    )

from rest_framework import filters


from ..models import Post , Like , Comment , Bookmark
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser , MultiPartParser
from rest_framework.exceptions import PermissionDenied , NotAuthenticated
from rest_framework.views import Http404
from rest_framework.pagination import CursorPagination
from rest_framework.generics import RetrieveAPIView , ListAPIView



# a pagination class for posts and comments to extends of
class PostCursorPagination(CursorPagination):
    ordering = "-createdAt"
    page_size = 10

# GET , POST , DELETE
class PostViews(APIView , PostCursorPagination):
    # getting all posts
    def get(self , request , format=None):
        
        posts = Post.objects.all()
        # gets paginated query set

        result = self.paginate_queryset(posts , request , view=self)

        # context is for getting the logged in user in PostSerializer methods 
        serializer = PostSerializer(result , many=True, context={"request": request})
        
        # paginated response
        return self.get_paginated_response(serializer.data)

    # creating new post
    def post(self , request , format=None):
        
        # check if user provided jwt token
        if request.user.is_authenticated:

            # check if logged in user(jwt token) is the provided user in post data
            if request.user.id != int(request.data["user"]):
                raise PermissionDenied
        
            # creates an instance of new post
            serializer = CreatePostSerializer(data=request.data)

            if serializer.is_valid():
                post = serializer.save()

                # if comment contains media
                if request.FILES:

                    # if this is true we can edit data
                    request.data._mutable = True
                    # set post field in data
                    request.data["post"] = post.id
                    # we make it false for securtiy reason
                    

                    mediaserializer =  MediaSerializer(data=request.data)

                    if mediaserializer.is_valid():

                        # uses create method in MediaSerializer class
                        mediaserializer.create(request.data , postInstance=post)
                        
                    
                        postSerializer = PostSerializer(post , context={"request": request})
                        # returns whole post with images that uploaded

                        return Response(postSerializer.data , status=status.HTTP_201_CREATED)
                    
                    #  if uploaded file is not image type, the saved post will be deleted and a respone returns
                    post.delete()

                    return Response(mediaserializer.errors , status=status.HTTP_400_BAD_REQUEST)
                
                # if there was no files just saves the post
                return Response(serializer.data , status=status.HTTP_201_CREATED)
            
            # if post credentials was not valid
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
            request.data._mutable = False
        # if user not provided jwt token in header
        else:
            raise NotAuthenticated
        
    # deleting a post
    def delete(self, request , format=None):

        # check if user provided jwt token
        if request.user.is_authenticated:
            try:
                # checks if post exists
                post = Post.objects.get(id=request.data["id"])

            except Post.DoesNotExist:
                return Response({"message":"post not found"} , status=status.HTTP_404_NOT_FOUND)
            
            # checks if the logged in user (jwt token) is the owner of the post 
            if post.user.id != request.user.id:
                raise PermissionDenied
            

            post.delete()

            return Response({"message":"post deleted successfully"} , status=status.HTTP_200_OK)
        
        # if user not provided jwt token in header
        else:
            raise NotAuthenticated


class SearchView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["caption" , "user__username"] 
    pagination_class = PostCursorPagination

# getting single post
class PostDetailView(RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

# GET , POST , DELETE
class CommentView(APIView , PostCursorPagination):

    # getting comments of a post
    def get(self, request, pk , format=None):

        comments = Comment.objects.filter(repliedTo=pk)

        # getting paginated queryset
        result = self.paginate_queryset(comments , request , view=self)        

        # context is for getting the logged in user in PostSerializer methods 
        serializer = PostSerializer(result , many=True , context={"request": request})

        # sending a paginated response
        return self.get_paginated_response(serializer.data)
    
    # creating new comment
    def post(self , request , pk , format=None):
        
        # checks if user is provided jwt token (logged in)
        if request.user.is_authenticated:

            try:
                Post.objects.get(id=pk)
            except Post.DoesNotExist:
                raise Http404

            # checks if logged in user is the one that requested
            if request.user.id != int(request.data["user"]):
                raise PermissionDenied


            
            # if this is true we can edit data
            request.data._mutable = True
            # set the url param in repliedTo field
            request.data["repliedTo"] = int(pk) 
            request.data["isReply"] = True
            request.data._mutable = False
         
            serializer = CommentSerializer(data=request.data)

            if serializer.is_valid():
                comment = serializer.save()


                commentSerializer = PostSerializer(comment, context={"request": request})

                # if comment contains media
                if request.FILES:

                    # sets comment id in request data
                    request.data._mutable = True
                    request.data["post"] = comment.id
                    request.data._mutable = False
                    mediaserializer =  MediaSerializer(data=request.data)

                    if mediaserializer.is_valid():
                        # use create method in MediaSerializer
                        mediaserializer.create(request.data , postInstance=comment)

                        postSerializer = PostSerializer(comment , context={"request": request})

                        # returns whole post with images that uploaded
                        return Response(postSerializer.data , status=status.HTTP_201_CREATED)
                    
                    #  if uploaded file is not image type the saved post will be deleted and a respone returns
                    comment.delete()
                    return Response(mediaserializer.errors , status=status.HTTP_400_BAD_REQUEST)
                
                return Response(commentSerializer.data , status=status.HTTP_201_CREATED)
            
            # bad request 
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

        # if user not provided hwt token (not logged in)
        else:
            raise NotAuthenticated
        
    # deleting a post
    def delete(self , request, pk , format=None):
        # if user is logged in 
        if request.user.is_authenticated:
            try:
                # checks if comments is exists
                comment = Comment.objects.get(id=request.data["id"])

            # if post not found 
            except Comment.DoesNotExist:
                return Response({"message":"comment not found"} , status=status.HTTP_404_NOT_FOUND)
            
            # checks if user who requested is the logged in user
            if comment.user.id != request.user.id:
                raise PermissionDenied
            
            comment.delete()

            return Response({"message":"comment deleted successfully"} , status=status.HTTP_200_OK)
        else:
            raise NotAuthenticated

# get a user's posts
class UserPostListView(ListAPIView):
    serializer_class = PostSerializer

    lookup_field = "username"

    pagination_class = PostCursorPagination

    def get_queryset(self):
        return Post.objects.filter(user__username=self.kwargs["username"])
    
# POST , DELETE
class LikePostView(APIView):
    

    def post(self , request , format=None):
        
        # check if user not liked post before
        

        # check if user is logged in 
        if request.user.is_authenticated:

            serializer = LikePostSerializer(data=request.data)

        
            if serializer.is_valid():
                # if user provided in post data is not the logged in user
                if request.user.id != int(request.data["user"]):
                    raise PermissionDenied
                
                # checks if user liked post before and unlike it
                try:
                    likeInstance = Like.objects.get(user=request.user.id , post=request.data["post"])
                    likeInstance.delete()
                    return Response({"message": "post removed from your likes successfully"} , status=status.HTTP_200_OK)
                
                # if didn't like post before creates a like record in db
                except Like.DoesNotExist:
                    serializer.save()
                    return Response({"message": "liked post"} , status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
        # if user is not logged in
        else:
            raise NotAuthenticated
        

# POST , GET
class BoookmarkView(APIView , PostCursorPagination):

    def post(self , request , format=None):

        if request.user.is_authenticated:

            serializer = CreateBookmarkSerializer(data=request.data)

            if serializer.is_valid():
                if request.user.id != int(request.data["user"]):
                    raise PermissionDenied
            

                try:
                    # if already bookmarkd removes it
                    bookmarkInstance = Bookmark.objects.get(user=request.data["user"] , post=request.data["post"])
                    bookmarkInstance.delete()
                    return Response({"message": "post removed from your bookmarks"} , status=status.HTTP_200_OK)

                except Bookmark.DoesNotExist:
                    # if does not exist adds it
                    serializer.save()
                    return Response({"message": "post added to your bookmakrs"} , status=status.HTTP_201_CREATED)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        # if user is not logged in
        else:
            raise NotAuthenticated
        

    def get(self , request , format=None):
        
        if request.user.is_authenticated:
            posts = Bookmark.objects.filter(user=request.user.id)
            paginatedQueryset = self.paginate_queryset(posts , request , view=self)
            serialzer = BookmarkSerializer(paginatedQueryset , many=True , context={"request": request})

            return self.get_paginated_response(serialzer.data)

        else:
            raise NotAuthenticated
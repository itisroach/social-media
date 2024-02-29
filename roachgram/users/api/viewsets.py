from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSeralizer

@api_view(["POST"])
def createUser(request):
    serializer = UserSeralizer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.create(request.data)
    return Response(serializer.data)



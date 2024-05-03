from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from users.models import FollowUser
from .models import Room
from users.models import User
from django.http import Http404
from django.db.models import Q

@login_required
def chat(request):

    if request.method == "POST":
        reciverId = request.POST.get("receiver")
        return redirect("chat-room" , f"{request.user.id}-{reciverId}")

    followedUsers = FollowUser.objects.filter(follower=request.user)
    
    context = {
        "available_users_to_chat": followedUsers
    }

    return render(request , "chatPage.html" , context)


@login_required
def chatRoom(request , room_name):
    try:
        # make reverse room_name. we reverse that because there might be same room but diffrent receivers and not creating new record in db
        reveresedRoomName = room_name.split("-")[::-1]
        otherRoomName = "-".join(reveresedRoomName)
        print(otherRoomName)
        room = Room.objects.get(Q(name=room_name) | Q(name=otherRoomName))
    except Room.DoesNotExist:
        room = Room(name=room_name)
        room.save()

    try:
        # room name is created by sender's id (logged in user) and receiver's id and like this sender-receiver
        receiverId = room_name.split("-")[1]
        receiver = User.objects.get(id=receiverId)
    except User.DoesNotExist:
        raise Http404

    context = {
        "room_name": room.name,
        "receiver": receiver
    }
    return render(request , "chatRoom.html" , context)
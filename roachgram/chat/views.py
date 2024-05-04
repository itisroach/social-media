from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from users.models import FollowUser
from .models import Room , Message
from users.models import User
from django.http import Http404
from django.db.models import Q

@login_required
def chat(request):

    if request.method == "POST":
        reciverId = request.POST.get("receiver")
        return redirect("chat-room" , f"{request.user.id}-{reciverId}")

    followedUsers = FollowUser.objects.filter(follower=request.user)
    chats = Message.objects.filter(Q(room__sender=request.user) | Q(room__receiver=request.user)).order_by("-createdAt").last()
    
    context = {
        "available_users_to_chat": followedUsers,
        "message": chats
    }

    return render(request , "chatPage.html" , context)


@login_required
def chatRoom(request , room_name):
    try:
        # room name is created by sender's id (logged in user) and receiver's id and like this sender-receiver
        ids = room_name.split("-")
        # remove logged in user from ids list
        ids.remove(str(request.user.id))
        # 1 item will remain which is another user excep logged in user
        receiverId = ids[0]
        receiver = User.objects.get(id=receiverId)
    except User.DoesNotExist:
        raise Http404
    
    try:
        # make reverse room_name. we reverse that because there might be same room but diffrent receivers and not creating new record in db
        reveresedRoomName = room_name.split("-")[::-1]
        otherRoomName = "-".join(reveresedRoomName)
        # check if one of room names exists
        room = Room.objects.get(Q(name=room_name) | Q(name=otherRoomName))
    except Room.DoesNotExist:
        room = Room(name=room_name , sender=request.user , receiver=receiver)
        room.save()

    messages = Message.objects.filter(room=room)
    
    context = {
        "room_name": room.name,
        "receiver": receiver,
        "chat_messages": messages 
    }
    return render(request , "chatRoom.html" , context)
from django.contrib import admin
from .models import User, FollowUser , NotificationType , Notification
# Register your models here.
admin.site.register(User)
admin.site.register(Notification)
admin.site.register(NotificationType)
admin.site.register(FollowUser)
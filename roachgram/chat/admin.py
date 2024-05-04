from django.contrib import admin
from .models import Room , Message , ConnectionHistory

admin.site.register(Room)
admin.site.register(ConnectionHistory)
admin.site.register(Message)

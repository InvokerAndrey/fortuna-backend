from django.contrib import admin

from .models import PlayerTransaction, RoomTransaction


admin.site.register(PlayerTransaction)
admin.site.register(RoomTransaction)

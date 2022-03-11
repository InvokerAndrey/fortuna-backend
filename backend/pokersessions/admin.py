from django.contrib import admin

from .models import Session, RoomSession


admin.site.register(Session)
admin.site.register(RoomSession)

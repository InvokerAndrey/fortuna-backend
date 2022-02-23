from django.db import models

from .enums import PlayerTransactionEnum, RoomTransactionEnum


class PlayerTransaction(models.Model):
    type = models.IntegerField(choices=PlayerTransactionEnum.choices())
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    player = models.ForeignKey(to='users.Player', on_delete=models.CASCADE)
    admin = models.ForeignKey(to='users.Admin', on_delete=models.CASCADE)


class RoomTransaction(models.Model):
    type = models.IntegerField(choices=RoomTransactionEnum.choices())
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    player = models.ForeignKey(to='users.Player', on_delete=models.CASCADE)
    room = models.ForeignKey(to='rooms.PlayerRoom', on_delete=models.CASCADE)

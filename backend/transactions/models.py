from django.db import models
from django.utils import timezone

from .enums import PlayerTransactionTypeEnum, RoomTransactionTypeEnum


class PlayerTransaction(models.Model):
    type = models.IntegerField(choices=PlayerTransactionTypeEnum.choices())
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    player = models.ForeignKey(to='users.Player', on_delete=models.CASCADE)
    admin = models.ForeignKey(to='users.Admin', on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.type} : {self.player}'


class RoomTransaction(models.Model):
    type = models.IntegerField(choices=RoomTransactionTypeEnum.choices())
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    player = models.ForeignKey(to='users.Player', on_delete=models.CASCADE)
    room = models.ForeignKey(to='rooms.PlayerRoom', on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.type} : {self.player}'

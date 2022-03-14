from django.db import models
from django.utils import timezone


class Session(models.Model):
    date = models.DateTimeField(default=timezone.now)
    player = models.ForeignKey(to='users.Player', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date} : {self.player.user.get_full_name()}'


class RoomSession(models.Model):
    room = models.ForeignKey(to='rooms.PlayerRoom', on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    # Сколько денег выиграл/проиграл
    result = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.room.room.name} : {self.session}'
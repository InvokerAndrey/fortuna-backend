from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # image = models.ImageField()
    description = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.name


class PlayerRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    player = models.ForeignKey(to='users.Player', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.room.name} : {self.player.user.get_full_name()}'

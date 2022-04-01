from django.db import models
from django.contrib.auth.models import User


class Fund(models.Model):
    """ Админский фонд на всю эту суету """
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return str(self.balance)


class Admin(models.Model):
    """ Расширение таблицы User для Админов """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    # Процент доли от общей прибыли в фонд
    # Доля фонда
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # Доля фонда одного админа за все время
    profit_share = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Player(models.Model):
    """ Расширение таблицы User для Игроков школы """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Доля профита игрока в %
    rate = models.IntegerField(default=40)
    # Деньги, которые зависли у пользователя. К примеру он не может депнуть на рум,
    # если ему до этого не зачислил деньги на игру админ
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Основной долг перед админом
    duty = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Профит за все время
    all_time_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Текущий профит
    current_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Зп за все время
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Принесенная прибыль админу за все время
    profit_to_admin = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Долг админу за профит
    admin_profit_share = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Своя доля профита
    self_profit_share = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.user.get_full_name()

# Generated by Django 4.0.2 on 2022-03-31 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_player_current_profit'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='profit_to_admin',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]

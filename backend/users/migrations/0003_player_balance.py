# Generated by Django 4.0.2 on 2022-03-15 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_player_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]

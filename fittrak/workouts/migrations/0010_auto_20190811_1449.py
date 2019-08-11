# Generated by Django 2.2.4 on 2019-08-11 14:49

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0009_auto_20190811_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='set',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=6),
        ),
    ]

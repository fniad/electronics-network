# Generated by Django 4.2.3 on 2024-02-22 13:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electronics_network', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='level',
            field=models.IntegerField(default=0, editable=False, verbose_name='уровень в иерархии'),
        ),
        migrations.AlterField(
            model_name='retailnetwork',
            name='level',
            field=models.IntegerField(editable=False, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)]),
        ),
    ]
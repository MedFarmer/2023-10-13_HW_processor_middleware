# Generated by Django 4.2.6 on 2023-10-10 05:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='balance',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='paypal',
            name='balance',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]

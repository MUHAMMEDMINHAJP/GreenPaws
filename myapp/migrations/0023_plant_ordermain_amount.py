# Generated by Django 3.0 on 2024-04-06 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0022_plant_ordermain_deldate'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant_ordermain',
            name='amount',
            field=models.CharField(default='', max_length=100),
        ),
    ]
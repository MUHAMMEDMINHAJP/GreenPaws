# Generated by Django 3.0 on 2024-03-25 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_deliveryaddress_payment_plant_ordermain_plant_ordersub'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plant_ordermain',
            name='ADDRESS',
        ),
    ]

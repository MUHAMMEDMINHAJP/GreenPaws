# Generated by Django 3.0 on 2024-04-02 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_assigned_order_payment_plant_ordermain_plant_ordersub'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='PLANT_ORDERMAIN',
        ),
        migrations.RemoveField(
            model_name='plant_ordermain',
            name='ADDRESS',
        ),
        migrations.RemoveField(
            model_name='plant_ordermain',
            name='SHOP',
        ),
        migrations.RemoveField(
            model_name='plant_ordermain',
            name='USER',
        ),
        migrations.RemoveField(
            model_name='plant_ordersub',
            name='PLANT',
        ),
        migrations.RemoveField(
            model_name='plant_ordersub',
            name='PLANT_ORDERMAIN',
        ),
        migrations.DeleteModel(
            name='Assigned_order',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='Plant_ordermain',
        ),
        migrations.DeleteModel(
            name='Plant_ordersub',
        ),
    ]

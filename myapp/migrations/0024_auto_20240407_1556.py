# Generated by Django 3.2.25 on 2024-04-07 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0023_plant_ordermain_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryboy',
            name='latitude',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deliveryboy',
            name='longitude',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pet',
            name='details',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='plant',
            name='details',
            field=models.CharField(max_length=1000),
        ),
    ]
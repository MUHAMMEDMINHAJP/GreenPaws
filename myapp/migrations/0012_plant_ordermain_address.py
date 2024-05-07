# Generated by Django 3.0 on 2024-03-25 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant_ordermain',
            name='ADDRESS',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.DeliveryAddress'),
            preserve_default=False,
        ),
    ]
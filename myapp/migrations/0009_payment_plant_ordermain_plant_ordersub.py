# Generated by Django 3.0 on 2024-03-25 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20240325_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plant_ordermain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=30)),
                ('SHOP', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Shop')),
                ('USER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.User')),
            ],
        ),
        migrations.CreateModel(
            name='Plant_ordersub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=30)),
                ('PLANT', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Plant')),
                ('PLANT_ORDERMAIN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Plant_ordermain')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PLANT_ORDERMAIN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Plant_ordermain')),
            ],
        ),
    ]

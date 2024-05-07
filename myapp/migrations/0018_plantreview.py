# Generated by Django 3.0 on 2024-04-05 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_auto_20240405_1108'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plantreview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('review', models.CharField(max_length=300)),
                ('rating', models.CharField(max_length=300)),
                ('SHOP', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Shop')),
                ('USER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.User')),
            ],
        ),
    ]
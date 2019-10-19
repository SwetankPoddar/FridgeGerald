# Generated by Django 2.2.6 on 2019-10-19 15:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fridgeManager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FridgeFoodItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('best_before', models.DateField(default=datetime.date.today)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fridgeManager.food_item')),
                ('fridge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foodItems', to='fridgeManager.food_item')),
            ],
        ),
        migrations.CreateModel(
            name='Fridge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

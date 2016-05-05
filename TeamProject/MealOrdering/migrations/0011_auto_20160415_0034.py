# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('MealOrdering', '0010_dishunpaid'),
    ]

    operations = [
        migrations.CreateModel(
            name='DishHistory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('number', models.DecimalField(max_digits=3, decimal_places=1, default=1)),
                ('createTime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('belonging', models.ForeignKey(to='MealOrdering.Customer', related_name='pending_customer')),
                ('dish', models.ForeignKey(to='MealOrdering.Dish', related_name='pending_dish')),
            ],
        ),
        migrations.RemoveField(
            model_name='dishpending',
            name='belonging',
        ),
        migrations.RemoveField(
            model_name='dishpending',
            name='dish',
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='zipcode',
            field=models.DecimalField(max_digits=3, blank=True, decimal_places=0, default=0),
        ),
        migrations.DeleteModel(
            name='DishPending',
        ),
    ]

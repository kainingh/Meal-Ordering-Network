# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('MealOrdering', '0009_auto_20160414_0017'),
    ]

    operations = [
        migrations.CreateModel(
            name='DishUnPaid',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('number', models.DecimalField(decimal_places=1, max_digits=3, default=1)),
                ('createTime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('belonging', models.ForeignKey(related_name='unpaid_customer', to='MealOrdering.Customer')),
                ('dish', models.ForeignKey(related_name='unpaid_dish', to='MealOrdering.Dish')),
            ],
        ),
    ]

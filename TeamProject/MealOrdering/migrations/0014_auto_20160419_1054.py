# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('MealOrdering', '0013_auto_20160417_1128'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryOrder',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('wholeMoney', models.DecimalField(default=0, decimal_places=0, max_digits=10)),
                ('createTime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='PendingOrder',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('wholeMoney', models.DecimalField(default=0, decimal_places=0, max_digits=10)),
                ('createTime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.AddField(
            model_name='wholeorder',
            name='restaurantName',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='cvv',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='expire',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='city',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='state',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='zipcode',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='dish',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='phoneNumber',
            field=models.DecimalField(decimal_places=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='pendingorder',
            name='belonging',
            field=models.ForeignKey(to='MealOrdering.Restaurant'),
        ),
        migrations.AddField(
            model_name='pendingorder',
            name='dishes',
            field=models.ManyToManyField(to='MealOrdering.DishHistory'),
        ),
        migrations.AddField(
            model_name='historyorder',
            name='belonging',
            field=models.ForeignKey(to='MealOrdering.Restaurant'),
        ),
        migrations.AddField(
            model_name='historyorder',
            name='dishes',
            field=models.ManyToManyField(to='MealOrdering.DishHistory'),
        ),
    ]

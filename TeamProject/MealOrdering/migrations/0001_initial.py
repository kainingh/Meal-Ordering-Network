# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentsOnDish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=200)),
                ('createTime', models.DateTimeField(default=datetime.datetime.now, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CommentsOnRest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=200)),
                ('createTime', models.DateTimeField(default=datetime.datetime.now, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=30)),
                ('cvv', models.CharField(max_length=10)),
                ('zipcode', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=100)),
                ('createTime', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('photo', models.ImageField(upload_to='customer-photo', blank=True)),
                ('phoneNumber', models.CharField(max_length=20, blank=True)),
                ('belonging', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=400, blank=True)),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('rating', models.DecimalField(default=0, max_digits=3, decimal_places=1, blank=True)),
                ('rateNumber', models.DecimalField(default=0, max_digits=10, decimal_places=0, blank=True)),
                ('numberTotoal', models.DecimalField(default=0, max_digits=10, decimal_places=0, blank=True)),
                ('createTime', models.DateTimeField(default=datetime.datetime.now, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DishPending',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.DecimalField(default=1, max_digits=3, decimal_places=1)),
                ('createTime', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('belonging', models.ForeignKey(related_name='pending_customer', to='MealOrdering.Customer')),
                ('dish', models.ForeignKey(related_name='pending_dish', to='MealOrdering.Dish')),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=100)),
                ('createTime', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('belonging', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PositionForRest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=200, blank=True)),
                ('coordinateX', models.DecimalField(max_digits=3, decimal_places=0)),
                ('coordinateY', models.DecimalField(max_digits=3, decimal_places=0)),
            ],
        ),
        migrations.CreateModel(
            name='PositionForUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=200, blank=True)),
                ('coordinateX', models.DecimalField(max_digits=3, decimal_places=0)),
                ('coordinateY', models.DecimalField(max_digits=3, decimal_places=0)),
                ('belonging', models.ForeignKey(to='MealOrdering.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('phoneNumber', models.CharField(max_length=20)),
                ('rating', models.DecimalField(default=0, max_digits=3, decimal_places=0, blank=True)),
                ('rateNumber', models.DecimalField(default=0, max_digits=10, decimal_places=0, blank=True)),
                ('numberTotal', models.DecimalField(default=0, max_digits=10, decimal_places=0, blank=True)),
                ('photo', models.ImageField(upload_to='restaurant-photo', blank=True)),
                ('createTime', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('belonging', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='positionforrest',
            name='belonging',
            field=models.ForeignKey(to='MealOrdering.Restaurant'),
        ),
        migrations.AddField(
            model_name='dish',
            name='belonging',
            field=models.ForeignKey(to='MealOrdering.Restaurant'),
        ),
        migrations.AddField(
            model_name='creditcard',
            name='belonging',
            field=models.ForeignKey(to='MealOrdering.Customer'),
        ),
        migrations.AddField(
            model_name='commentsonrest',
            name='belonging',
            field=models.ForeignKey(related_name='comment_restaurant', to='MealOrdering.Restaurant'),
        ),
        migrations.AddField(
            model_name='commentsonrest',
            name='commenter',
            field=models.ForeignKey(related_name='customer_comment_rest', to='MealOrdering.Customer'),
        ),
        migrations.AddField(
            model_name='commentsondish',
            name='belonging',
            field=models.ForeignKey(related_name='comment_dish', to='MealOrdering.Dish'),
        ),
        migrations.AddField(
            model_name='commentsondish',
            name='commenter',
            field=models.ForeignKey(related_name='customer_comment_dish', to='MealOrdering.Customer'),
        ),
    ]

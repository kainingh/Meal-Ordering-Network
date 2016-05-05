# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MealOrdering', '0011_auto_20160415_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantaddress',
            name='zipcode',
            field=models.DecimalField(decimal_places=0, blank=True, max_digits=3, default=0),
        ),
    ]

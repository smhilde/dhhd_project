# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0002_auto_20141120_2004'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='customer',
            new_name='customers',
        ),
        migrations.RenameField(
            model_name='plan',
            old_name='feature',
            new_name='features',
        ),
        migrations.AddField(
            model_name='plan',
            name='elevation_file',
            field=models.CharField(default='1565_250.jpg', verbose_name='Elevation File', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plan',
            name='floorplan_file',
            field=models.CharField(default='1742layout.jpg', verbose_name='Floor Plan File', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='acct_num',
            field=models.IntegerField(verbose_name='account number', unique=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='area',
            field=models.PositiveIntegerField(verbose_name='Square Feet'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='bath',
            field=models.FloatField(verbose_name='Bathrooms'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='bed',
            field=models.FloatField(verbose_name='Bedrooms'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='ceiling',
            field=models.FloatField(null=True, verbose_name='Ceiling Height'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='depth',
            field=models.FloatField(null=True, verbose_name='House Depth'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='floor',
            field=models.PositiveIntegerField(default=1, verbose_name='Number of Floors'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='garage',
            field=models.PositiveIntegerField(verbose_name='Garage Size'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='height',
            field=models.FloatField(null=True, verbose_name='House Height'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='number',
            field=models.PositiveIntegerField(verbose_name='Plan Number', unique=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='price',
            field=models.FloatField(null=True, verbose_name='Plan Price'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Published'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='width',
            field=models.FloatField(null=True, verbose_name='House Width'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('acct_num', models.IntegerField(verbose_name='account number')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('street_number', models.IntegerField()),
                ('street_name', models.CharField(max_length=250)),
                ('town', models.CharField(max_length=250)),
                ('state', models.CharField(max_length=250)),
                ('zip_code', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('number', models.PositiveIntegerField(unique=True, verbose_name='plan number')),
                ('title', models.CharField(null=True, unique=True, max_length=1000)),
                ('area', models.PositiveIntegerField(verbose_name='square feet')),
                ('bed', models.FloatField(verbose_name='bedrooms')),
                ('bath', models.FloatField(verbose_name='bathrooms')),
                ('floor', models.PositiveIntegerField(default=1, verbose_name='number of floors')),
                ('garage', models.PositiveIntegerField(verbose_name='number of garages')),
                ('width', models.FloatField(null=True, verbose_name='house width')),
                ('depth', models.FloatField(null=True, verbose_name='house width')),
                ('height', models.FloatField(null=True, verbose_name='house height')),
                ('ceiling', models.FloatField(null=True, verbose_name='ceiling height')),
                ('price', models.FloatField(null=True)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('customer', models.ManyToManyField(null=True, to='plan.Customer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpecialFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('room', models.CharField(max_length=100)),
                ('feature', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('usrid', models.CharField(unique=True, max_length=100)),
                ('usrpwd', models.CharField(max_length=100)),
                ('plan', models.ManyToManyField(to='plan.Plan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='plan',
            name='feature',
            field=models.ManyToManyField(null=True, to='plan.SpecialFeature'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='plan',
            field=models.ForeignKey(to='plan.Plan'),
            preserve_default=True,
        ),
    ]

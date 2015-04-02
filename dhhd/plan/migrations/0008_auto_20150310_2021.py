# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0007_plan_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Plan Active'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='plan',
            name='price',
            field=models.CharField(max_length=4, verbose_name='Plan Price', null=True),
            preserve_default=True,
        ),
    ]

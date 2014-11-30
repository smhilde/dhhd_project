# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0004_auto_20141126_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='number',
            field=models.CharField(verbose_name='Plan Number', unique=True, max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='plan',
            name='title',
            field=models.CharField(null=True, unique=True, max_length=100),
            preserve_default=True,
        ),
    ]

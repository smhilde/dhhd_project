# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0005_auto_20141128_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='living',
            field=models.PositiveIntegerField(verbose_name='Living Areas', default=1),
            preserve_default=True,
        ),
    ]

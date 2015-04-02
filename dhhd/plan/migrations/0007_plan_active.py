# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0006_plan_living'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

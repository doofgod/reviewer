# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofilepicture',
            name='image',
            field=models.ImageField(upload_to=b'profiles'),
            preserve_default=True,
        ),
    ]

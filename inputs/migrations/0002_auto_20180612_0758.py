# Generated by Django 2.0.6 on 2018-06-12 11:58

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inputs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]

# Generated by Django 2.0.6 on 2018-06-28 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0006_auto_20180627_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]

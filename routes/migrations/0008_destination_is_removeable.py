# Generated by Django 2.0.6 on 2018-06-28 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0007_destination_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='is_removeable',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 2.0.6 on 2018-06-27 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0005_auto_20180624_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]

# Generated by Django 2.2.6 on 2019-11-04 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotels',
            name='parking',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='hotels',
            name='smart_tv',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='hotels',
            name='wifi',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.0.1 on 2020-06-06 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20200606_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
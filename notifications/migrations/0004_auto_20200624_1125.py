# Generated by Django 3.0.1 on 2020-06-24 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_notification_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='inside_link',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='movie_link',
            field=models.TextField(blank=True, null=True),
        ),
    ]

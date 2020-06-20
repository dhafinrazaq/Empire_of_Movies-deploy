# Generated by Django 3.0.1 on 2020-06-04 03:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0006_review_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='downvoters',
            field=models.ManyToManyField(blank=True, related_name='discussion_downvoted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='discussion',
            name='downvoters_counter',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='discussion',
            name='upvoters',
            field=models.ManyToManyField(blank=True, related_name='discussion_upvoted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='discussion',
            name='upvoters_counter',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
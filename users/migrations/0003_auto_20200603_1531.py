# Generated by Django 3.0.1 on 2020-06-03 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_review_author'),
        ('users', '0002_customuser_follows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='follows',
        ),
        migrations.AddField(
            model_name='customuser',
            name='follows',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='articles.Movie'),
        ),
    ]

# Generated by Django 2.0.6 on 2018-07-04 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_profile_sexual_pref'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='instagram',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='profile',
            name='snapchat',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]

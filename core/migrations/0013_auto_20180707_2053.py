# Generated by Django 2.0.6 on 2018-07-07 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='token',
            old_name='token',
            new_name='key',
        ),
    ]
# Generated by Django 2.0.1 on 2018-03-12 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='item_ID',
            new_name='item_id',
        ),
    ]

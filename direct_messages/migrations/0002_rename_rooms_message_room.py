# Generated by Django 4.1.7 on 2023-03-05 02:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('direct_messages', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='rooms',
            new_name='room',
        ),
    ]
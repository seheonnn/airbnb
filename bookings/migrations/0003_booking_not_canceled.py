# Generated by Django 4.1.7 on 2023-04-02 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_alter_booking_experience_alter_booking_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='not_canceled',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 4.0 on 2023-04-05 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='like',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='room',
            name='amenities',
            field=models.ManyToManyField(related_name='rooms', to='rooms.Amenity'),
        ),
    ]
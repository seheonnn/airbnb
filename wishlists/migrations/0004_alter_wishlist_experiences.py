# Generated by Django 4.0 on 2023-04-07 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiences', '0003_alter_experience_perks'),
        ('wishlists', '0003_alter_wishlist_experiences'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='experiences',
            field=models.ManyToManyField(blank=True, related_name='wishlists', to='experiences.Experience'),
        ),
    ]
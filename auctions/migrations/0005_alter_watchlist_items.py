# Generated by Django 4.2.5 on 2024-03-17 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='users', to='auctions.listing'),
        ),
    ]

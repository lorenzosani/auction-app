# Generated by Django 2.1.14 on 2019-11-20 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctionapp', '0004_item_start_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to='auctionapp/static/auctionapp/item_images'),
        ),
    ]
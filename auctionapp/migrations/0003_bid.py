# Generated by Django 2.1.14 on 2019-11-17 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctionapp', '0002_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time_placed', models.DateTimeField(auto_now_add=True)),
                ('bidder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctionapp.Member')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctionapp.Item')),
            ],
            options={
                'ordering': ['-amount'],
                'get_latest_by': '-time_placed',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='bids',
            field=models.ManyToManyField(through='auctionapp.Bid', to='auctionapp.Member'),
        ),
    ]

# Generated by Django 4.2.6 on 2023-10-30 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('closed', 'Closed'), ('cancelled', 'Cancelled')], default='open', max_length=10),
        ),
    ]

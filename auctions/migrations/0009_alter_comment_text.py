# Generated by Django 4.2.6 on 2023-10-30 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_auctionlisting_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=1024),
        ),
    ]

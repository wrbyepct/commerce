# Generated by Django 4.2.6 on 2023-10-24 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_auctionlisting_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='auctions/images/'),
        ),
    ]

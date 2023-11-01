# Generated by Django 4.2.6 on 2023-10-31 09:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_rename_text_comment_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=1024, validators=[django.core.validators.MinLengthValidator(1)]),
        ),
    ]
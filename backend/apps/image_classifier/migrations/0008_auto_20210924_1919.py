# Generated by Django 3.1.2 on 2021-09-24 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_classifier', '0007_auto_20210924_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='backend_address',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
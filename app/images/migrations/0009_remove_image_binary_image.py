# Generated by Django 4.0.8 on 2022-11-21 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0008_binaryimagelink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='binary_image',
        ),
    ]

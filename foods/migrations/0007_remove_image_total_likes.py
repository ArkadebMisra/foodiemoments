# Generated by Django 2.1.7 on 2019-04-19 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0006_image_total_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='total_likes',
        ),
    ]

# Generated by Django 3.0.7 on 2020-06-12 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='link',
            field=models.CharField(max_length=200),
        ),
    ]

# Generated by Django 2.0.3 on 2018-04-20 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tagging', '0002_auto_20180416_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentence',
            name='file_name',
            field=models.CharField(default=1, help_text='file_name', max_length=255),
        ),
    ]
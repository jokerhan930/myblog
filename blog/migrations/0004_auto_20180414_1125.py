# Generated by Django 2.0.2 on 2018-04-14 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180414_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(default='none', upload_to='blog/static/images'),
        ),
    ]

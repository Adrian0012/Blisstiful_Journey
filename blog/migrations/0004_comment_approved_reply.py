# Generated by Django 2.2.7 on 2020-05-30 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200530_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='approved_reply',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 2.2.3 on 2019-07-09 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0008_userdata_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='user_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]

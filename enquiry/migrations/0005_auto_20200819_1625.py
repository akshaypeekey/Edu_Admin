# Generated by Django 3.0.6 on 2020-08-19 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry', '0004_auto_20200819_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='notes',
            field=models.TextField(blank='True', null='True'),
        ),
    ]

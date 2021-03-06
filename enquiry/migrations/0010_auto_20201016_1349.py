# Generated by Django 3.0.6 on 2020-10-16 08:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry', '0009_auto_20200922_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='source',
            field=models.TextField(blank='True', null='True'),
            preserve_default='True',
        ),
        migrations.AlterField(
            model_name='admission',
            name='date',
            field=models.DateField(default=datetime.date(2020, 10, 16)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='batch_date',
            field=models.DateField(default=datetime.date(2020, 10, 16)),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='address',
            field=models.TextField(blank='True', null='True'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='college',
            field=models.CharField(blank='True', max_length=30, null='True'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='email',
            field=models.EmailField(blank='True', max_length=254, null='True'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='enquiry_date',
            field=models.DateField(default=datetime.date(2020, 10, 16)),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='qualification',
            field=models.CharField(blank='True', max_length=20, null='True'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(default=datetime.date(2020, 10, 16)),
        ),
    ]

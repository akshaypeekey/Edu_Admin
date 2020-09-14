# Generated by Django 3.0.6 on 2020-08-10 07:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry', '0002_auto_20200809_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='date',
            field=models.DateField(default=datetime.date(2020, 8, 10)),
        ),
        migrations.AlterField(
            model_name='admission',
            name='enquiry_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enquiry.Enquiry'),
        ),
        migrations.AlterField(
            model_name='batch',
            name='batch_date',
            field=models.DateField(default=datetime.date(2020, 8, 10)),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='enquiry_date',
            field=models.DateField(default=datetime.date(2020, 8, 10)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(default=datetime.date(2020, 8, 10)),
        ),
    ]
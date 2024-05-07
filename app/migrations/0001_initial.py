# Generated by Django 5.0.3 on 2024-05-03 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('contact_details', models.TextField()),
                ('address', models.TextField()),
                ('vendor_code', models.CharField(max_length=50, unique=True)),
                ('on_time_delivery_rate', models.FloatField(default=0.0)),
                ('quality_rating_avg', models.FloatField(default=0.0)),
                ('average_response_time', models.FloatField(default=0.0)),
                ('fulfillment_rate', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='purchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_number', models.CharField(max_length=20, unique=True)),
                ('order_date', models.DateTimeField()),
                ('delivery_date', models.DateTimeField()),
                ('items', models.JSONField()),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceles')], max_length=50)),
                ('quality_rating', models.FloatField(blank=True, null=True)),
                ('issue_date', models.DateTimeField()),
                ('acknowledgement_date', models.DateTimeField(blank=True, null=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('on_time_delivery_rate', models.FloatField()),
                ('quality_rating_avg', models.FloatField()),
                ('average_response_time', models.FloatField()),
                ('fulfillment_rete', models.FloatField()),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.vendor')),
            ],
        ),
    ]

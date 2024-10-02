# Generated by Django 5.1.1 on 2024-10-02 11:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_order_total_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransportationFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=10.0, max_digits=6)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='transportation_fee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.transportationfee'),
        ),
    ]
# Generated by Django 5.0.2 on 2024-09-16 17:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_information'),
    ]

    operations = [
        migrations.AddField(
            model_name='information',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='informations', to='product.product'),
        ),
    ]

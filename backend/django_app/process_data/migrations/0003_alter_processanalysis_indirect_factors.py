# Generated by Django 5.1.4 on 2025-01-20 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process_data', '0002_processanalysis_indirect_costs_factor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processanalysis',
            name='indirect_factors',
            field=models.JSONField(blank=True, help_text='List of indirect cost factors with name, cost, and percentage values', null=True),
        ),
    ]

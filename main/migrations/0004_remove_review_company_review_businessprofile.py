# Generated by Django 5.0.6 on 2024-06-17 15:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_company_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='company',
        ),
        migrations.AddField(
            model_name='review',
            name='BusinessProfile',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='main.businessprofile'),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.0.6 on 2024-06-27 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_page', '0003_accion'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='huella',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

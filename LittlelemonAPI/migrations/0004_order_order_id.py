# Generated by Django 5.1.4 on 2025-01-15 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittlelemonAPI', '0003_alter_menuitems_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.IntegerField(default=1, max_length=3),
            preserve_default=False,
        ),
    ]

# Generated by Django 2.2.1 on 2020-02-21 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20200221_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='car',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.Contact'),
        ),
    ]

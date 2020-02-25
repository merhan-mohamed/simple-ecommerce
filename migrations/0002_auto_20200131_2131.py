# Generated by Django 2.2.6 on 2020-01-31 19:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='once_click_purchasing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='strip_customer_id',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
# Generated by Django 2.2.6 on 2020-02-21 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='address_type',
        ),
    ]
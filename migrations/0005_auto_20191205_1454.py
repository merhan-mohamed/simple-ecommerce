# Generated by Django 2.2.6 on 2019-12-05 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_categorey_catdes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CATName', models.CharField(max_length=50, verbose_name='Category Name')),
                ('CATDes', models.TextField(verbose_name='Description')),
                ('CATImg', models.ImageField(upload_to='category/', verbose_name='Image')),
                ('CATParent', models.ForeignKey(blank=True, limit_choices_to={'CATParent__isnull': True}, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.Category', verbose_name='Main Category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product_Alternatives',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PALNAlternatives', models.ManyToManyField(related_name='alternative_products', to='product.Product')),
                ('PALNProduct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_product', to='product.Product')),
            ],
        ),
        migrations.DeleteModel(
            name='Categorey',
        ),
    ]

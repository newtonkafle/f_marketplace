# Generated by Django 4.2.3 on 2023-07-27 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]

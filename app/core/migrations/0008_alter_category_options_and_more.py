# Generated by Django 4.2.3 on 2023-07-25 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_category_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='food_title',
            new_name='product_title',
        ),
    ]

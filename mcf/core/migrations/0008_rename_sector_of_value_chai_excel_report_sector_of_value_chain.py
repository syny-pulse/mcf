# Generated by Django 5.0.3 on 2024-04-06 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_rename_date_arrears_start_excel_report_date_of_default_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='excel_report',
            old_name='SECTOR_OF_VALUE_CHAI',
            new_name='SECTOR_OF_VALUE_CHAIN',
        ),
    ]
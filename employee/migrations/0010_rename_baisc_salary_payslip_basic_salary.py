# Generated by Django 5.0.1 on 2024-01-30 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0009_employee_email_alter_employee_account_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payslip',
            old_name='baisc_salary',
            new_name='basic_salary',
        ),
    ]

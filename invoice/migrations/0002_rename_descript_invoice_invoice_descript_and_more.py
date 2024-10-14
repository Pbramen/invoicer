# Generated by Django 5.1.2 on 2024-10-14 02:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_users', '0002_alter_customer_user'),
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='descript',
            new_name='invoice_descript',
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='title',
            new_name='invoice_title',
        ),
        migrations.RenameField(
            model_name='workorder',
            old_name='descript',
            new_name='order_descript',
        ),
        migrations.RenameField(
            model_name='workorder',
            old_name='title',
            new_name='order_title',
        ),
        migrations.AlterField(
            model_name='workitem',
            name='job_site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom_users.address'),
        ),
    ]
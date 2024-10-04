# Generated by Django 5.1.1 on 2024-10-02 22:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='phonenumber',
            old_name='value',
            new_name='phone_number',
        ),
        migrations.AddField(
            model_name='emailaddresse',
            name='contact_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_users.contact'),
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='contact_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_users.contact'),
        ),
        migrations.AddField(
            model_name='physicaladdresse',
            name='contact_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_users.contact'),
        ),
        migrations.AlterField(
            model_name='physicaladdresse',
            name='city',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='physicaladdresse',
            name='street',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='physicaladdresse',
            name='zipcode',
            field=models.CharField(max_length=12),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_alert', models.CharField(db_comment='Time before due date when email notification is sent', max_length=24)),
                ('contact_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_users.contact')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]

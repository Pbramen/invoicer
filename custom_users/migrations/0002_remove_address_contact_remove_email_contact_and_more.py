# Generated by Django 5.1.2 on 2024-10-10 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='email',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='phonenumber',
            name='contact',
        ),
        migrations.AddField(
            model_name='contact',
            name='address',
            field=models.ManyToManyField(to='custom_users.address'),
        ),
        migrations.AddField(
            model_name='contact',
            name='email',
            field=models.ManyToManyField(to='custom_users.email'),
        ),
        migrations.AddField(
            model_name='contact',
            name='phoneNumber',
            field=models.ManyToManyField(to='custom_users.phonenumber'),
        ),
    ]
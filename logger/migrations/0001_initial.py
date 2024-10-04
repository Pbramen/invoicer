# Generated by Django 5.1.1 on 2024-10-02 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EndpointRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FileMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=64)),
                ('version', models.IntegerField(default=0)),
                ('source', models.CharField(max_length=50, null=True)),
                ('extension', models.CharField(max_length=32)),
                ('file_size', models.FloatField(db_comment="in MB's")),
                ('checksum', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParserError',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SystemError',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
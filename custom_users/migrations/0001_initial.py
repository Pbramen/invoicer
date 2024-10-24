# Generated by Django 5.1.2 on 2024-10-19 17:20

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('J', 'Job Site'), ('M', 'Home'), ('C', 'Company'), ('O', 'Other')], default='M', max_length=12, null=True)),
                ('street', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=45)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('KY', 'Kentucky'), ('OH', 'Ohio'), ('AK', 'Alaska'), ('LA', 'Louisiana'), ('OK', 'Oklahoma'), ('AZ', 'Arizona'), ('ME', 'Maine'), ('OR', 'Oregon'), ('AR', 'Arkansas'), ('MD', 'Maryland'), ('PA', 'Pennsylvania'), ('MA', 'Massachusetts'), ('NH', 'New Hampshire'), ('CA', 'California'), ('MI', 'Michigan'), ('RI', 'Rhode Island'), ('CO', 'Colorado'), ('MN', 'Minnesota'), ('SC', 'South Carolina'), ('CT', 'Connecticut'), ('MS', 'Mississippi'), ('SD', 'South Dakota'), ('DE', 'Delaware'), ('MO', 'Missouri'), ('TN', 'Tennessee'), ('MT', 'Montana'), ('TX', 'Texas'), ('FL', 'Florida'), ('NE', 'Nebraska'), ('GA', 'Georgia'), ('NV', 'Nevada'), ('UT', 'Utah'), ('VT', 'Vermont'), ('HI', 'Hawaii'), ('NJ', 'New Jersey'), ('VA', 'Virginia'), ('ID', 'Idaho'), ('NM', 'New Mexico'), ('IL', 'Illinois'), ('NY', 'New York'), ('WA', 'Washington'), ('IN', 'Indiana'), ('NC', 'North Carolina'), ('WV', 'West Virginia'), ('IA', 'Iowa'), ('ND', 'North Dakota'), ('WI', 'Wisconsin'), ('KS', 'Kansas'), ('WY', 'Wyoming')], default='AL', max_length=2)),
                ('zipcode', models.CharField(max_length=12)),
                ('lat', models.FloatField(default=None, null=True)),
                ('lng', models.FloatField(default=None, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('P', 'Personal'), ('W', 'Work'), ('A', 'Alternative'), ('O', 'Other')], default='P', max_length=1)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('M', 'Mobile'), ('H', 'Home'), ('W', 'Work'), ('O', 'Other')], default='M', max_length=1)),
                ('phone_number', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(message='Phone number must be in the format $xxx xxx-xxxx.', regex='^[0-9]{3} [0-9]{3}-[0-9]{4}$')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('address', models.ManyToManyField(to='custom_users.address')),
                ('email', models.ManyToManyField(to='custom_users.email')),
                ('phoneNumber', models.ManyToManyField(to='custom_users.phonenumber')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=64)),
                ('is_registered', models.BooleanField()),
                ('customer_contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom_users.contact')),
            ],
        ),
        migrations.CreateModel(
            name='UserContactInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert_timeframes', models.CharField(db_comment='Time before due date when email notification is sent', default='30d', max_length=24)),
                ('contact', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_contact', to='custom_users.contact')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, default='0', editable=False, max_length=22)),
                ('vendor_name', models.CharField(max_length=64)),
                ('status', models.BooleanField(default=True)),
                ('vendor_contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_contact', to='custom_users.contact')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(default='E', max_length=1)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='custom_users.contact')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom_users.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='VendorCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_LUT', to='custom_users.customer')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_LUT', to='custom_users.vendor')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='vendor_to_customer',
            field=models.ManyToManyField(through='custom_users.VendorCustomer', to='custom_users.vendor'),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-16 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='otp_code',
        ),
    ]

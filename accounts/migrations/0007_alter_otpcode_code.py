# Generated by Django 5.1.1 on 2024-10-16 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_otpcode_remove_customuser_otp_verified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='code',
            field=models.PositiveIntegerField(),
        ),
    ]
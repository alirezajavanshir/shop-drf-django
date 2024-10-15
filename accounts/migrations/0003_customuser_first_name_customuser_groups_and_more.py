# Generated by Django 5.1.1 on 2024-10-15 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_is_active_customuser_is_superuser'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='نام'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='نام خانوادگی'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.TextField(blank=True, verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='کاربر کارمندی'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='سوپرکاربر'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='otp_code',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='کد OTP'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='otp_verified',
            field=models.BooleanField(default=False, verbose_name='تأیید شده OTP'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=15, unique=True, verbose_name='شماره تلفن'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, verbose_name='کد پستی'),
        ),
    ]
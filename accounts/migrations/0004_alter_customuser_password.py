# Generated by Django 5.1.1 on 2024-10-16 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_first_name_customuser_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=20, verbose_name='رمز عبور'),
        ),
    ]
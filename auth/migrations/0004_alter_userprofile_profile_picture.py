# Generated by Django 5.0.7 on 2024-08-01 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_custom_auth', '0003_rename_profile_pic_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics'),
        ),
    ]

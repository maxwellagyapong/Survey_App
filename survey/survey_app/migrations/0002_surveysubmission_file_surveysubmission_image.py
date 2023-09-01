# Generated by Django 4.2.4 on 2023-09-01 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveysubmission',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='media/submitted-files/', verbose_name='File'),
        ),
        migrations.AddField(
            model_name='surveysubmission',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/submitted-images/', verbose_name='Image'),
        ),
    ]

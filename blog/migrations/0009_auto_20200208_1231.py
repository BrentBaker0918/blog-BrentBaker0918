# Generated by Django 2.2.2 on 2020-02-08 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]

# Generated by Django 4.1 on 2022-08-14 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='petition',
            name='description',
            field=models.TextField(max_length=2000, null=True),
        ),
    ]

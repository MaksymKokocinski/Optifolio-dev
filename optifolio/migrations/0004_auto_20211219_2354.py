# Generated by Django 3.2.2 on 2021-12-19 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('optifolio', '0003_alter_visdata_title2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticname',
            name='tic_id',
        ),
        migrations.AlterField(
            model_name='ticname',
            name='tic_sym',
            field=models.CharField(blank=True, max_length=10, primary_key=True, serialize=False),
        ),
    ]

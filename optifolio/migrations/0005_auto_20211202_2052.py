# Generated by Django 3.2.7 on 2021-12-02 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('optifolio', '0004_auto_20211116_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('portfolio_id', models.AutoField(primary_key=True, serialize=False)),
                ('portfolio_title', models.CharField(blank=True, max_length=200, null=True)),
                ('user_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='optifolio.customer')),
            ],
        ),
        migrations.AddField(
            model_name='visdata',
            name='portfolio_id',
            field=models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.SET_DEFAULT, to='optifolio.portfolio'),
        ),
    ]

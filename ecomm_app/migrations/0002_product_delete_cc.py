# Generated by Django 5.0 on 2024-01-08 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('pdetails', models.CharField(max_length=100)),
                ('cat', models.ImageField(upload_to='')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.DeleteModel(
            name='CC',
        ),
    ]

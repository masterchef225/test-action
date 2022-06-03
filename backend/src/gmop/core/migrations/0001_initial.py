# Generated by Django 3.2.13 on 2022-05-27 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.TextField(blank=True, default='', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
            ],
        ),
    ]
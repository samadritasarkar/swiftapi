# Generated by Django 2.0.5 on 2018-06-08 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('container', models.CharField(max_length=30)),
                ('object', models.CharField(max_length=30)),
            ],
        ),
    ]

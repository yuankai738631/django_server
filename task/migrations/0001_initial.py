# Generated by Django 4.1.7 on 2023-03-21 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('taskName', models.CharField(max_length=40)),
                ('projectName', models.CharField(max_length=125)),
                ('status', models.IntegerField(default=0)),
                ('creator', models.CharField(max_length=20)),
            ],
        ),
    ]
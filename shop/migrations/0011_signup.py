# Generated by Django 2.2.3 on 2020-02-16 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_delete_signup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Firstname', models.CharField(max_length=50)),
                ('Lastname', models.CharField(max_length=50)),
                ('email', models.CharField(default='', max_length=70)),
                ('Password', models.CharField(default='', max_length=70)),
            ],
        ),
    ]
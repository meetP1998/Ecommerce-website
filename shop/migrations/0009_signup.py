# Generated by Django 2.2.3 on 2020-02-16 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20190809_1430'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Username', models.CharField(max_length=50)),
                ('email', models.CharField(default='', max_length=70)),
                ('Password', models.CharField(default='', max_length=70)),
            ],
        ),
    ]
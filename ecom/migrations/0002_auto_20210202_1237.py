# Generated by Django 3.1.5 on 2021-02-02 07:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=30)),
                ('mobile', models.CharField(max_length=12)),
                ('gender', models.CharField(max_length=6)),
                ('dateofbirth', models.DateField()),
                ('address', models.CharField(max_length=70)),
                ('country', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=20)),
                ('login_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.usertype')),
            ],
        ),
        migrations.DeleteModel(
            name='User_type',
        ),
    ]

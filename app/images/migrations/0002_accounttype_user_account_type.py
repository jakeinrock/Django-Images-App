# Generated by Django 4.0.8 on 2022-11-16 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('is_basic', models.BooleanField(default=False)),
                ('is_premium', models.BooleanField(default=False)),
                ('is_enterprise', models.BooleanField(default=False)),
                ('is_custom', models.BooleanField(default=False)),
                ('thumb_size1', models.IntegerField()),
                ('thumb_size2', models.IntegerField(blank=True, null=True)),
                ('link_to_original', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='account_type',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='users', to='images.accounttype'),
        ),
    ]
# Generated by Django 4.1.3 on 2022-12-07 13:48

import uuid

import django.core.validators
import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=12, region='RU', unique=True, verbose_name='phone')),
                ('provider_code', models.IntegerField(validators=[django.core.validators.MinValueValidator(900), django.core.validators.MaxValueValidator(999)], verbose_name='provider code')),
                ('tz', models.CharField(default='UTC+03:00', max_length=50, verbose_name='client time zone')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'db_table': 'notice_client',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_at', models.DateTimeField(verbose_name='start')),
                ('msg', models.CharField(max_length=160, verbose_name='message')),
                ('stop_at', models.DateTimeField(verbose_name='stop')),
            ],
            options={
                'verbose_name': 'Mailing',
                'verbose_name_plural': 'Mailings',
                'db_table': 'notice_mailing',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='tag name')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('status', models.CharField(choices=[('created', 'Created'), ('sended', 'Success'), ('error', 'Error'), ('cancelled', 'Canceled')], default='created', max_length=50, verbose_name='status')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='notice.client', verbose_name='client')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='notice.mailing', verbose_name='mailing')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'db_table': 'notice_message',
            },
        ),
        migrations.AddField(
            model_name='mailing',
            name='tag',
            field=models.ManyToManyField(to='notice.tag'),
        ),
        migrations.AddField(
            model_name='client',
            name='tag',
            field=models.ManyToManyField(to='notice.tag'),
        ),
    ]

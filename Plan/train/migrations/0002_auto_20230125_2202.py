# Generated by Django 2.2.16 on 2023-01-25 17:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('train', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('Vi', 'Vi'), ('I1', 'I1'), ('I2', 'I2'), ('I3', 'I3'), ('I4', 'I4'), ('I4+I5', 'I4+I5'), ('I5', 'I5'), ('I6', 'I6'), ('30', '30 суток'), ('Зима', 'Зима'), ('Лето', 'Лето'), ('-', '-'), ('Vi*', 'Vi*'), ('I1*', 'I1*'), ('I2*', 'I2*')], default='Vi', max_length=2, verbose_name='Тип инспекции')),
                ('mileage', models.IntegerField(blank=True, null=True, verbose_name='Планируемый пробег')),
                ('number', models.IntegerField(blank=True, null=True, verbose_name='Номер инспекции по порядку')),
                ('comment', models.CharField(blank=True, max_length=150, null=True, verbose_name='Примечание')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='donemaidate',
            name='comment',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Примечание'),
        ),
        migrations.AlterField(
            model_name='donemaidate',
            name='maintenance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance', to='train.Maintenance', verbose_name='Вид ТО'),
        ),
        migrations.AlterField(
            model_name='donemaidate',
            name='place',
            field=models.CharField(choices=[('ЕКБ', 'Екатеринбург'), ('ЧЛБ', 'Челябинск'), ('Пермь', 'Пермь'), ('МСК', 'Москва'), ('СПБ', 'Санкт-Петербург'), ('Сочи', 'Сочи'), ('Крюково', 'Крюково')], default='ЕКБ', max_length=2, verbose_name='Место проведения'),
        ),
        migrations.AlterField(
            model_name='planmaidate',
            name='maintenance',
            field=models.CharField(choices=[('Vi', 'Vi'), ('I1', 'I1'), ('I2', 'I2'), ('I3', 'I3'), ('I4', 'I4'), ('I4+I5', 'I4+I5'), ('I5', 'I5'), ('I6', 'I6'), ('30', '30 суток'), ('Зима', 'Зима'), ('Лето', 'Лето'), ('-', '-'), ('Vi*', 'Vi*'), ('I1*', 'I1*'), ('I2*', 'I2*')], default='Vi', max_length=2, verbose_name='Вид ТО'),
        ),
        migrations.AlterField(
            model_name='planmaidate',
            name='place',
            field=models.CharField(blank=True, choices=[('Vi', 'Vi'), ('I1', 'I1'), ('I2', 'I2'), ('I3', 'I3'), ('I4', 'I4'), ('I4+I5', 'I4+I5'), ('I5', 'I5'), ('I6', 'I6'), ('30', '30 суток'), ('Зима', 'Зима'), ('Лето', 'Лето'), ('-', '-'), ('Vi*', 'Vi*'), ('I1*', 'I1*'), ('I2*', 'I2*')], default='ЕКБ', max_length=2, verbose_name='Место проведения'),
        ),
        migrations.AddConstraint(
            model_name='donemaidate',
            constraint=models.UniqueConstraint(fields=('train', 'maintenance'), name='train_maintenance'),
        ),
        migrations.AddField(
            model_name='maintenance',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maintenance_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='maintenance',
            index=models.Index(fields=['created'], name='train_maint_created_6afcbd_idx'),
        ),
    ]

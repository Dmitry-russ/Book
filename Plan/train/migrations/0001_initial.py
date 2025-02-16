# Generated by Django 2.2.16 on 2024-08-20 05:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=150, verbose_name='Короткое описание')),
                ('text', models.CharField(blank=True, max_length=500, verbose_name='Полное описание')),
                ('file', models.FileField(blank=True, null=True, upload_to='cases/', verbose_name='Прикрепленный документ')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cases', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Serial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('serial', models.TextField(max_length=5, unique=True, validators=[django.core.validators.MinLengthValidator(3, message='Должно быть больше двух символов.')], verbose_name='Серия')),
                ('slug', models.SlugField(max_length=5, unique=True, validators=[django.core.validators.MinLengthValidator(3, message='Должно быть больше двух символов.')], verbose_name='Слаг')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='serial', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('number', models.CharField(max_length=5, validators=[django.core.validators.MinLengthValidator(3, message='Должно быть больше двух символов.')], verbose_name='Номер')),
                ('renter', models.CharField(blank=True, max_length=5, null=True, verbose_name='Арендатор')),
                ('mileage', models.IntegerField(blank=True, null=True, verbose_name='Пробег на дату')),
                ('mileage_date', models.DateField(blank=True, null=True, verbose_name='Дата считывания пробега')),
                ('day_mileage', models.IntegerField(blank=True, null=True, verbose_name='Среднесуточный пробег')),
                ('image', models.ImageField(blank=True, null=True, upload_to='Plan/', verbose_name='Фото')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='train', to=settings.AUTH_USER_MODEL)),
                ('serial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='train', to='train.Serial', verbose_name='Серия')),
            ],
            options={
                'ordering': ['serial', 'number'],
            },
        ),
        migrations.CreateModel(
            name='PlanMaiDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('maintenance', models.CharField(choices=[('Vi', 'Vi'), ('I1', 'I1'), ('I2', 'I2'), ('I3', 'I3'), ('I4', 'I4'), ('I4+I5', 'I4+I5'), ('I5', 'I5'), ('I6', 'I6'), ('R1', 'R1'), ('R2', 'R2'), ('R3', 'R3'), ('R4', 'R4'), ('I5+I6', 'I5+I6'), ('R1+I5', 'R1+I5'), ('30', '30 суток'), ('Зима', 'Зима'), ('Лето', 'Лето'), ('-', '-'), ('Vi*', 'Vi*'), ('I1*', 'I1*'), ('I2*', 'I2*')], default='Vi', max_length=2, verbose_name='Вид ТО')),
                ('date_one', models.DateField(verbose_name='Дата начала ТО')),
                ('date_two', models.DateField(verbose_name='Дата окончания ТО')),
                ('place', models.CharField(blank=True, choices=[('Vi', 'Vi'), ('I1', 'I1'), ('I2', 'I2'), ('I3', 'I3'), ('I4', 'I4'), ('I4+I5', 'I4+I5'), ('I5', 'I5'), ('I6', 'I6'), ('R1', 'R1'), ('R2', 'R2'), ('R3', 'R3'), ('R4', 'R4'), ('I5+I6', 'I5+I6'), ('R1+I5', 'R1+I5'), ('30', '30 суток'), ('Зима', 'Зима'), ('Лето', 'Лето'), ('-', '-'), ('Vi*', 'Vi*'), ('I1*', 'I1*'), ('I2*', 'I2*')], default='ЕКБ', max_length=2, verbose_name='Место проведения')),
                ('mileage', models.IntegerField(blank=True, verbose_name='Пробег')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plan', to=settings.AUTH_USER_MODEL)),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan', to='train.Train', verbose_name='Поезд')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('Vi', 'Vi'), ('I1', 'I1'), ('I2', 'I2'), ('I3', 'I3'), ('I4', 'I4'), ('I4+I5', 'I4+I5'), ('I5', 'I5'), ('I6', 'I6'), ('R1', 'R1'), ('R2', 'R2'), ('R3', 'R3'), ('R4', 'R4'), ('I5+I6', 'I5+I6'), ('R1+I5', 'R1+I5'), ('30', '30 суток'), ('Зима', 'Зима'), ('Лето', 'Лето'), ('-', '-'), ('Vi*', 'Vi*'), ('I1*', 'I1*'), ('I2*', 'I2*')], default='Vi', max_length=5, verbose_name='Тип инспекции')),
                ('mileage', models.IntegerField(blank=True, null=True, verbose_name='Планируемый пробег')),
                ('number', models.IntegerField(blank=True, null=True, verbose_name='Номер инспекции по порядку')),
                ('comment', models.CharField(blank=True, max_length=150, null=True, verbose_name='Примечание')),
                ('order', models.BooleanField(default=True, verbose_name='Плановый инспекции по порядку')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maintenance_list', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150)),
                ('image', models.ImageField(upload_to='images/')),
                ('default', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='image', to=settings.AUTH_USER_MODEL)),
                ('cases', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='train.Cases')),
            ],
        ),
        migrations.CreateModel(
            name='DoneMaiDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('maintenance_date', models.DateField(verbose_name='Дата')),
                ('place', models.CharField(choices=[('ЕКБ', 'Екатеринбург'), ('ЧЛБ', 'Челябинск'), ('Пермь', 'Пермь'), ('МСК', 'Москва'), ('СПБ', 'Санкт-Петербург'), ('Сочи', 'Сочи'), ('Крюково', 'Крюково'), ('КЛГ', 'Калининград')], default='ЕКБ', max_length=30, verbose_name='Место проведения')),
                ('mileage', models.IntegerField(verbose_name='Пробег')),
                ('comment', models.CharField(blank=True, max_length=150, null=True, verbose_name='Примечание')),
                ('musthave', models.BooleanField(default=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maintenance', to=settings.AUTH_USER_MODEL)),
                ('maintenance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance', to='train.Maintenance', verbose_name='Вид ТО')),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance', to='train.Train', verbose_name='Поезд')),
            ],
            options={
                'ordering': ['mileage'],
            },
        ),
        migrations.AddField(
            model_name='cases',
            name='train',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases', to='train.Train', verbose_name='Поезд'),
        ),
        migrations.AddConstraint(
            model_name='train',
            constraint=models.UniqueConstraint(fields=('serial', 'number'), name='serial_number'),
        ),
        migrations.AddIndex(
            model_name='serial',
            index=models.Index(fields=['created'], name='train_seria_created_635435_idx'),
        ),
        migrations.AddIndex(
            model_name='planmaidate',
            index=models.Index(fields=['created'], name='train_planm_created_d8a887_idx'),
        ),
        migrations.AddConstraint(
            model_name='donemaidate',
            constraint=models.UniqueConstraint(fields=('train', 'maintenance_date', 'maintenance'), name='train_maintenance_date'),
        ),
        migrations.AddIndex(
            model_name='cases',
            index=models.Index(fields=['created'], name='train_cases_created_d0fe67_idx'),
        ),
    ]

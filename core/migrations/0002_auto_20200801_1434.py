# Generated by Django 3.0.7 on 2020-08-01 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='genero',
            field=models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], default='M', max_length=10, null=True, verbose_name='Genero'),
        ),
        migrations.AddField(
            model_name='profile',
            name='idade',
            field=models.IntegerField(blank=True, default=18, null=True, verbose_name='Idade'),
        ),
    ]

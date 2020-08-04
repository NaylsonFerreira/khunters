# Generated by Django 3.0.7 on 2020-08-03 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200801_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='apelido',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Como gostaria de ser chamado?'),
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='nome',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome completo'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='genero',
            field=models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], default='M', max_length=10, null=True, verbose_name='Gênero'),
        ),
    ]

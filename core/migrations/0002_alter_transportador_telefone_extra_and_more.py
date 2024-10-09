# Generated by Django 5.1.1 on 2024-10-09 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportador',
            name='telefone_extra',
            field=models.CharField(blank=True, max_length=16, verbose_name='Telefone Extra'),
        ),
        migrations.AlterField(
            model_name='transportador',
            name='telefone_fixo',
            field=models.CharField(blank=True, max_length=16, verbose_name='Telefone Fixo'),
        ),
    ]

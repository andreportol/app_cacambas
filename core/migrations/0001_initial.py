# Generated by Django 5.1.2 on 2024-10-15 17:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Regiao_CG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_regiao', models.CharField(choices=[('SEGREDO', 'SEGREDO'), ('PROSA', 'PROSA'), ('CENTRO', 'CENTRO'), ('IMBIRUSSU', 'IMBIRUSSU'), ('LAGOA', 'LAGOA'), ('ANHANDUIZINHO', 'ANHANDUIZINHO'), ('BANDEIRA', 'BANDEIRA')], max_length=13, unique=True, verbose_name='Região')),
            ],
            options={
                'verbose_name': 'Região',
                'verbose_name_plural': 'Regiões',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Atualização')),
                ('nome_usuario', models.CharField(max_length=150, verbose_name='Nome de usuário')),
                ('telefone', models.CharField(max_length=10, verbose_name='Telefone')),
                ('logradouro', models.CharField(max_length=200, verbose_name='Logradouro')),
                ('nr_porta', models.CharField(max_length=5, verbose_name='Número de porta')),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('bairro', models.CharField(max_length=100, verbose_name='Bairro')),
                ('latitude', models.CharField(max_length=13, verbose_name='Latitude')),
                ('longitude', models.CharField(max_length=13, verbose_name='Longitude')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
        ),
        migrations.CreateModel(
            name='Bairros_CG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_bairro', models.CharField(max_length=150, verbose_name='Bairro')),
                ('nome_regiao_regioes', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.regiao_cg', to_field='nome_regiao', verbose_name='Nome Região')),
            ],
            options={
                'verbose_name': 'Bairro',
                'verbose_name_plural': 'Bairros',
            },
        ),
        migrations.CreateModel(
            name='Transportador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Atualização')),
                ('nome_fantasia', models.CharField(max_length=150, unique=True, verbose_name='Nome transportador')),
                ('telefone_fixo', models.CharField(blank=True, max_length=16, verbose_name='Telefone Fixo')),
                ('telefone_extra', models.CharField(blank=True, max_length=16, verbose_name='Telefone Extra')),
                ('telefone_celular', models.CharField(blank=True, max_length=16, verbose_name='Telefone celular')),
                ('email', models.CharField(max_length=150, verbose_name='E-mail')),
                ('logradouro', models.CharField(max_length=200, verbose_name='Logradouro')),
                ('nr_porta', models.CharField(max_length=5, verbose_name='Número de porta')),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('bairro', models.CharField(max_length=100, verbose_name='Bairro')),
                ('regiao', models.CharField(choices=[('SEGREDO', 'SEGREDO'), ('PROSA', 'PROSA'), ('CENTRO', 'CENTRO'), ('IMBIRUSSU', 'IMBIRUSSU'), ('LAGOA', 'LAGOA'), ('ANHANDUIZINHO', 'ANHANDUIZINHO'), ('BANDEIRA', 'BANDEIRA')], max_length=13, verbose_name='Região')),
                ('is_ativo', models.BooleanField(default=False, verbose_name='Ativo')),
                ('qtd_cacambas', models.IntegerField(verbose_name='Quantidade caçambas')),
                ('regioes_trabalho', models.ManyToManyField(to='core.regiao_cg', verbose_name='Regiões de Trabalho')),
            ],
            options={
                'verbose_name': 'Transportador',
                'verbose_name_plural': 'Transportadores',
            },
        ),
    ]

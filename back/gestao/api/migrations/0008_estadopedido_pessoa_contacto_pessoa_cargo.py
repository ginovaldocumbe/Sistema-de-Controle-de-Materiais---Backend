# Generated by Django 4.2 on 2023-05-11 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_fornecedor_alter_entrada_id_material_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apelido', models.CharField(max_length=70)),
                ('nomes', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=10)),
                ('acesso', models.IntegerField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Contacto_Pessoa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contacto', models.IntegerField(max_length=9)),
                ('id_pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pessoa')),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
                ('id_pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pessoa')),
            ],
        ),
    ]

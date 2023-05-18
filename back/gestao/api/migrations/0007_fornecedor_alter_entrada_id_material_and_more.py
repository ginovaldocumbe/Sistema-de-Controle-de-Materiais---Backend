# Generated by Django 4.2 on 2023-05-11 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_entrada'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(max_length=250)),
                ('endereco', models.TextField(max_length=250)),
            ],
        ),
        migrations.AlterField(
            model_name='entrada',
            name='id_material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.material'),
        ),
        migrations.AlterField(
            model_name='material',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.categoria'),
        ),
        migrations.CreateModel(
            name='Fornecimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(max_length=100)),
                ('dataFornecimento', models.DateTimeField()),
                ('id_entrada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.entrada')),
                ('id_fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fornecedor')),
            ],
        ),
        migrations.CreateModel(
            name='Contacto_Fornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contacto', models.IntegerField(max_length=9)),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fornecedor')),
            ],
        ),
    ]

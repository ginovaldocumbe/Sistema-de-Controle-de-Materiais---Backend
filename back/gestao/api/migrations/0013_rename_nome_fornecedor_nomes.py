# Generated by Django 4.2 on 2023-05-17 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_fornecedor_apelido_alter_fornecedor_nome'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fornecedor',
            old_name='nome',
            new_name='nomes',
        ),
    ]

# Generated by Django 4.2 on 2023-05-18 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_remove_pedidomaterial_id_pesssoa_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estadopedido',
            name='id_pessoa',
        ),
    ]

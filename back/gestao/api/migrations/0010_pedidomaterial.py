# Generated by Django 4.2 on 2023-05-11 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_contacto_fornecedor_contacto_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidoMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataPedido', models.DateTimeField()),
                ('quant_Pedida', models.IntegerField()),
                ('estadoPedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.estadopedido')),
                ('id_Pesssoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pessoa')),
                ('id_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.material')),
            ],
        ),
    ]
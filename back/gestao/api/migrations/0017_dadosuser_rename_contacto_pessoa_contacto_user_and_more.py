# Generated by Django 4.2 on 2023-05-18 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0016_conta'),
    ]

    operations = [
        migrations.CreateModel(
            name='DadosUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sexo', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1, null=True)),
                ('data_nascimento', models.DateField()),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cargo')),
            ],
        ),
        migrations.RenameModel(
            old_name='Contacto_Pessoa',
            new_name='Contacto_User',
        ),
        migrations.DeleteModel(
            name='Conta',
        ),
        migrations.AddField(
            model_name='dadosuser',
            name='contacto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.contacto_user'),
        ),
        migrations.AddField(
            model_name='dadosuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

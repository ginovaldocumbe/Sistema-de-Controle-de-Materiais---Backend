from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(null=True, blank=True, max_length=250)

    def __str__(self):
        return self.nome


class Material(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(max_length=250)
    quant_min = models.IntegerField(null=True, blank=True)
    quant_disponivel = models.IntegerField(null=True, blank=True)
    cod_barras = models.IntegerField(null=True, blank=True)
    categoria = models.ForeignKey(
        Categoria, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Entrada(models.Model):
    dataEntrada = models.DateTimeField()
    quant_entrada = models.IntegerField()
    dataValidade = models.DateField()
    id_material = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return self.dataEntrada


class Fornecedor(models.Model):
    apelido = models.CharField(max_length=100, null=True)
    nomes = models.CharField(max_length=100, null=True)
    descricao = models.TextField(max_length=250)
    endereco = models.TextField(max_length=250)

    def __str__(self):
        return self.apelido


class Contacto_Fornecedor(models.Model):
    contacto = models.IntegerField()
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.contacto


class Fornecimento(models.Model):
    descricao = models.TextField(max_length=100)
    dataFornecimento = models.DateTimeField()
    id_entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE)
    id_fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao


class EstadoPedido(models.Model):
    estado = models.CharField(max_length=50)
    def __str__(self):
        return self.estado


class PedidoMaterial(models.Model):
    dataPedido = models.DateTimeField()
    quant_Pedida = models.IntegerField()
    id_material = models.ForeignKey(Material, on_delete=models.CASCADE)
    id_pessoa = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, blank=True, null=True
    )
    estadoPedido = models.ForeignKey(EstadoPedido, on_delete=models.CASCADE)

    def __repr__(self):
        return self.dataPedido


class Cargo(models.Model):
    descricao = models.CharField(max_length=100)
    id_pessoa = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.descricao


class Contacto_Pessoa(models.Model):
    contacto = models.IntegerField()
    id_pessoa = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.contacto

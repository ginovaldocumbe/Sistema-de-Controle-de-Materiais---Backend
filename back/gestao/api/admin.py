from django.contrib import admin
from .models import Material, Categoria,Entrada, PedidoMaterial,Fornecedor, Fornecimento, Contacto_Fornecedor,Contacto_User, Cargo, EstadoPedido, DadosUser
# Register your models here.


admin.site.register(Material)
admin.site.register(Categoria)
admin.site.register(Entrada)
admin.site.register(PedidoMaterial)
admin.site.register(Fornecedor)
admin.site.register(Fornecimento)
admin.site.register(Contacto_Fornecedor)
admin.site.register(Contacto_User)
admin.site.register(Cargo)
admin.site.register(EstadoPedido)
admin.site.register(DadosUser)

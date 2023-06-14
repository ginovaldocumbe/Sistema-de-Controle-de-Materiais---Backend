from django.urls import path

from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.endpoints),
    path('registo/', views.RegisterApi.as_view()),
    path('login/', views.LoginApi.as_view()),
    path('funcionario/', views.FuncionarioAPI.as_view()),
    
    #Endpoints do material 
    path('material/', views.MaterialAPI.as_view()),
    path('material/<str:id>', views.material_detalhes),

    path('categoria/', views.CategoriaAPI.as_view()),
    path('estado/', views.EstadoAPI.as_view()),
    path('entrada/', views.EntradaAPI.as_view()),
    path('pedido_material/', views.PedidoMaterialAPI.as_view()),
    path('fornecimento/', views.FornecimentoAPI.as_view()),
    path('cargo/', views.CargoAPI.as_view()),
    path('fornecedor/', views.FornecedorAPI.as_view()),
]
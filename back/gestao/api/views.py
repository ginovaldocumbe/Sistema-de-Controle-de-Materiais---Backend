from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import  HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Material, Categoria, Entrada, PedidoMaterial, Fornecimento, Cargo, Fornecedor
from .serializers import MaterialSerializer, RegisterSerializer, LoginSerializer, CategoriaSerializer, EntradaSerializer, UserSerializer,PedidoMaterialSerializer, FornecimentoSerializer, CargoSerializer, FornecedorSerializer, EstadoPedido, MyTokenObtainPairSerializer

from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def endpoints(request):
    data = ['messages', 'Finalmente consegui!!!']
    return Response(data)


class LoginApi(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'mensage': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=serializer.data['username'], password=serializer.data['password'])
        if not user:
            return Response({
                'status': False,
                'mensagem': 'Credenciais invalidas!',
            }, status.HTTP_400_BAD_REQUEST)

        print(user)
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'status': True,
            'mensagem': 'Usuario Logado!',
            'token': str(token)
        }, status.HTTP_201_CREATED)


class RegisterApi(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'mensage': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({
            'status': True,
            'mensagem': 'Usuario registado com sucesso!',
            'dados_usuario':serializer.data
        }, status.HTTP_201_CREATED)


# Post e o Get all dos materiais
class MaterialAPI(APIView):
    def get(self, request):
        data = Material.objects.all()
        serializer = MaterialSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        material = Material.objects.create(
            # categoria=request.data['categoria'],
            nome=request.data['nome'],
            descricao=request.data['descricao'],
            quant_min=request.data['quant_min'],
            quant_disponivel=request.data['quant_disponivel'],
            cod_barras=request.data['cod_barras']
        )
        serializer = MaterialSerializer(material, many=False)
        return Response(serializer.data)


@api_view(['GET', 'PUT', "DELETE"])
def material_detalhes(request, id):
    material = Material.objects.get(id=id)

    if request.method == 'GET':
        serializer = MaterialSerializer(material, many=False)
        return Response(serializer.data)

    if request.method == 'PUT':
        try:
            categori = Categoria.objects.get(id=request.data['categoria'])
            material.categoria = categori
        except:
            return HttpResponseNotFound({
                'status': False,
                'mensagem': 'Categoria nao encontrada!'
            }, status.HTTP_404_NOT_FOUND)

        material.nome = request.data['nome']
        material.descricao = request.data['descricao']
        material.quant_min = request.data['quant_min']
        material.quant_disponivel = request.data['quant_disponivel']
        material.cod_barras = request.data['cod_barras']

        material.save()

        serializer = MaterialSerializer(material, many=False)
        return Response(serializer.data)

    if request.method == 'DELETE':
        material.delete()
        return Response('Deletado com sucesso!')


class CategoriaAPI(APIView):
    def get(self, request):
        data = Categoria.objects.all()
        serializer = CategoriaSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = CategoriaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({
            'status': False,
            'mensagem': 'Erro ao registar os dados!',
            'erro': serializer.errors
        }, status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data
        obj = Categoria.objects.get(id=data['id'])
        serializer = CategoriaSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({
            'status': True,
            'mensagem': 'Erro ao actualizar dados!',
            'erro': serializer.errors
        }, status.HTTP_202_ACCEPTED)

    def delete(self, request):
        data = request.data
        obj = Categoria.objects.get(id=data['id'])
        obj.delete()
        return Response({
            'status': True,
            'mensagem': 'Categoria apagada com sucesso!!'
        }, status.HTTP_202_ACCEPTED)


class EntradaAPI(APIView):
    def get(self, request):
        data = Entrada.objects.all()
        serializer = EntradaSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        material = Material.objects.get(id=request.data['id_material'])
        entrada = Entrada.objects.create(

            dataEntrada=request.data['dataEntrada'],
            quant_entrada=request.data['quant_entrada'],
            dataValidade=request.data['dataValidade'],
            id_material=material
        )
        serializer = EntradaSerializer(entrada, many=False)
        return Response(serializer.data)

    def put(self, request):
        entrada = Entrada.objects.get(id=request.data['id'])
        material = Material.objects.get(id=request.data['id_material'])

        entrada.dataEntrada = request.data['dataEntrada'],
        entrada.quant_entrada = request.data['quant_entrada'],
        entrada.dataValidade = request.data['dataValidade'],
        entrada.id_material = material

        entrada.save()

        serializer = EntradaSerializer(entrada, many=False)
        return Response(serializer.data)

    def delete(self, request):
        data = request.data
        obj = Entrada.objects.get(id=data['id'])
        obj.delete()
        return Response({
            'status': True,
            'mensagem': 'Categoria apagada com sucesso!!'
        }, status.HTTP_202_ACCEPTED)


class PedidoMaterialAPI(APIView):
    def get(self, request):
        data = PedidoMaterial.objects.all()
        serializer = PedidoMaterialSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        material = Material.objects.get(id=request.data['id_material'])
        pessoa = User.objects.get(pk=request.data['id_Pessoa'])
        estado = EstadoPedido.objects.get(id=request.data['estadoPedido'])

        pedido = PedidoMaterial.objects.create(
            dataPedido=request.data['dataPedido'],
            quant_pedida=request.data['quant_pedida'],
            id_Material=material,
            id_Pessoa=pessoa,
            estadoPedido=estado
        )
        serializer = PedidoMaterialSerializer(pedido, many=False)
        return Response(serializer.data)

    def put(self, request):
        pedido = PedidoMaterial.objects.get(id=request.data['id'])
        material = Material.objects.get(id=request.data['id_material'])
        pessoa = User.objects.get(pk=request.data['id_pessoa'])
        estado = EstadoPedido.objects.get(id=request.data['estadoPedido'])

        print(material)
        pedido.dataPedido = request.data['dataPedido']
        pedido.quant_Pedida = request.data['quant_Pedida']
        pedido.id_material = material
        pedido.id_pessoa = pessoa
        pedido.estadoPedido = estado

        pedido.save()

        serializer = PedidoMaterialSerializer(pedido, many=False)
        return Response(serializer.data)

    def delete(self, request):
        data = request.data
        obj = PedidoMaterial.objects.get(id=data['id'])
        obj.delete()
        return Response({
            'status': True,
            'mensagem': 'Pedido apagada com sucesso!!'
        }, status.HTTP_202_ACCEPTED)


class FornecimentoAPI(APIView):
    def get(self, request):
        data = Fornecimento.objects.all()
        serializer = EntradaSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        entrada = Entrada.objects.get(id=request.data['id_entrada'])
        fornecedor = Fornecedor.objects.get(id=request.data['id_fornecedor'])

        fornecimento = Fornecimento.objects.create(

            descricao=request.data['descricao'],
            dataFornecimento=request.data['dataFornecimento'],
            id_entrada=entrada,
            id_fornecedor=fornecedor
        )
        serializer = FornecimentoSerializer(fornecimento, many=False)
        return Response(serializer.data)

    def put(self, request):
        fornecimento = Fornecimento.objects.get(id=request.data['id'])
        entrada = Entrada.objects.get(id=request.data['id_entrada'])
        fornecedor = Fornecedor.objects.get(id=request.data['id_fornecedor'])

        fornecimento.descricao = request.data['descricao'],
        fornecimento.dataFornecimento = request.data['dataFornecimento'],
        fornecimento.id_entrada = entrada,
        fornecimento.id_fornecedor = fornecedor

        fornecimento.save()

        serializer = EntradaSerializer(fornecimento, many=False)
        return Response(serializer.data)

    def delete(self, request):
        data = request.data
        obj = Entrada.objects.get(id=data['id'])
        obj.delete()
        return Response({
            'status': True,
            'mensagem': 'Categoria apagada com sucesso!!'
        }, status.HTTP_202_ACCEPTED)


class CargoAPI(APIView):
    def get(self, request):
        data = Cargo.objects.all()
        serializer = CargoSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        pessoa = User.objects.get(pk=request.data['id_pessoa'])
        cargo = Cargo.objects.create(
            descricao=request.data['descricao'],
            id_pessoa=pessoa
        )
        serializer = CargoSerializer(cargo, many=False)
        return Response(serializer.data)

    def put(self, request):
        cargo = Cargo.objects.get(id=request.data['id'])
        pessoa = User.objects.get(pk=request.data['id_pessoa'])

        cargo.descricao = request.data['descricao'],
        cargo.id_pessoa = pessoa

        cargo.save()

        serializer = CargoSerializer(cargo, many=False)
        return Response(serializer.data)

    def delete(self, request):
        data = request.data
        obj = Cargo.objects.get(id=data['id'])
        obj.delete()
        return Response({
            'status': True,
            'mensagem': 'Categoria apagada com sucesso!!'
        }, status.HTTP_202_ACCEPTED)


class FuncionarioAPI(APIView):
    def get(self, request):
        data =  User.objects.all()
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        pessoa = User.objects.get(pk=request.data['id_pessoa'])
        cargo = Cargo.objects.create(
            descricao=request.data['descricao'],
            id_pessoa=pessoa
        )
        serializer = CargoSerializer(cargo, many=False)
        return Response(serializer.data)

    def put(self, request):
        cargo = Cargo.objects.get(id=request.data['id'])
        pessoa = User.objects.get(pk=request.data['id_pessoa'])

        cargo.descricao = request.data['descricao'],
        cargo.id_pessoa = pessoa

        cargo.save()

        serializer = CargoSerializer(cargo, many=False)
        return Response(serializer.data)

    def delete(self, request):
        data = request.data
        obj = Cargo.objects.get(id=data['id'])
        obj.delete()
        return Response({
            'status': True,
            'mensagem': 'Categoria apagada com sucesso!!'
        }, status.HTTP_202_ACCEPTED)



class FornecedorAPI(APIView):
    def get(self, request):
        data = Fornecedor.objects.all()
        serializer = FornecedorSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = FornecedorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({
            'status': False,
            'mensagem': 'Erro ao registar os entrada!',
            'erro': serializer.errors
        }, status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data
        obj = Fornecedor.objects.get(id=data['id'])
        serializer = FornecedorSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({
            'status': True,
            'mensagem': 'Erro ao actualizar dados!',
            'erro': serializer.errors
        }, status.HTTP_202_ACCEPTED)

    def delete(self, request):
        data = request.data
        obj = Fornecedor.objects.get(id=data['id'])
        obj.delete()
        return Response({
            'status': True,
            'mensagem': 'Categoria apagada com sucesso!!'
        }, status.HTTP_202_ACCEPTED)


# @api_view(['GET', 'POST'])
# def material(request):
#     # data = ['Gino', 'Stelio', 'Cumbe']
#     if request.method == 'GET':
#         data = Material.objects.all()
#         serializer = MaterialSerializer(data, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         material = Material.objects.create(
#             nome=request.data['nome'],
#             descricao=request.data['descricao'],
#             quant_min=request.data['quant_min'],
#             quant_disponivel=request.data['quant_disponivel'],
#             cod_barras=request.data['cod_barras']
#         )
#         serializer = MaterialSerializer(material, many=False)
#         return Response(serializer.data)

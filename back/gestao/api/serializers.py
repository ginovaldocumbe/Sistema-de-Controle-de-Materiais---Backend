from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Material, Categoria, Entrada, PedidoMaterial, Fornecimento, Fornecedor, Cargo, EstadoPedido
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('O user ja existe bro!')

        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('O email ja existe bro!')
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class MaterialSerializer(ModelSerializer):
    categoria = CategoriaSerializer()
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Material
        fields = ['id', 'nome', 'descricao', 'quant_min',
                  'quant_disponivel', 'cod_barras', 'categoria']

    def update(self, validated_data):
        categoria_data = validated_data.pop('categoria')
        material = Material.objects.update(**validated_data)
        for categoria_data in categoria_data:
            Categoria.objects.update(material=material, **categoria_data)
        return material


class EntradaSerializer(ModelSerializer):
    id_material = MaterialSerializer()

    class Meta:
        model = Entrada
        fields = ['id', 'dataEntrada', 'quant_entrada',
                  'dataValidade', 'id_material']


class EstadoSerializer(ModelSerializer):
    class Meta:
        model = EstadoPedido
        fields = '__all__'


class PedidoMaterialSerializer(serializers.ModelSerializer):
    id_material = MaterialSerializer()
    id_pessoa = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    # id_pessoa = serializers.SerializerMethodField('_user')
    estadoPedido = EstadoSerializer()
  
    class Meta:
        model = PedidoMaterial
        fields = '__all__'


class FornecimentoSerializer(ModelSerializer):
    class Meta:
        model = Fornecimento
        fields = '__all__'


class CargoSerializer(ModelSerializer):
    id_pessoa = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Cargo
        fields = '__all__'


class FornecedorSerializer(ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'

    # def validate(self, data):
    #     if data['quant_min'] < 1:
    #      raise serializers.ValidationError('Adicione pelo menos uma quantidade minima!')
    #     return data

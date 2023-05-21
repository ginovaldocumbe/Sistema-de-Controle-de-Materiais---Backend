from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Material, Categoria, Entrada, PedidoMaterial, Fornecimento, Fornecedor, Cargo, EstadoPedido, DadosUser, Contacto_User
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

class UserSerializer(ModelSerializer):
    class Meta:
        model= User
        fields= '__all__'

class CargoSerializer(ModelSerializer):
    id_pessoa = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Cargo
        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    sexo = serializers.CharField()
    data_nascimento = serializers.DateField(input_formats=["%d-%m-%Y"])
    # contacto = serializers.IntegerField()
    # cargo = serializers.IntegerField()

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
            username=validated_data['username'], email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()

        pessoa = User.objects.get(pk = 1)
        carg = Cargo.objects.get(id=1)
        print("Cargo: ",carg)

 

        outros_dados = DadosUser.objects.create(
            sexo=validated_data['sexo'],
            data_nascimento=validated_data['data_nascimento'],
            # cargo=carg,
            user_id= pessoa
        )
        outros_dados.save()
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
    id_pessoa = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    # id_pessoa = serializers.SerializerMethodField('_user')
    estadoPedido = EstadoSerializer()

    class Meta:
        model = PedidoMaterial
        fields = '__all__'


class FornecimentoSerializer(ModelSerializer):
    class Meta:
        model = Fornecimento
        fields = '__all__'


class FornecedorSerializer(ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'

    # def validate(self, data):
    #     if data['quant_min'] < 1:
    #      raise serializers.ValidationError('Adicione pelo menos uma quantidade minima!')
    #     return data

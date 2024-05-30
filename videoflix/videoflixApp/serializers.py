from rest_framework import serializers
from .models import User,Video,Serie,Episode,UserFilmEvaluation,UserSerieEvaluation,MyListe,Category,CategoryListSeries,CategoryListFilm
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.db import transaction


# class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User    
        fields = ['id','username','email','short']
        
        
"""
Registers a new User, when all the given data are valid.
"""
class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)
  class Meta:
    model = User
    fields = ('username', 'password', 'password2','email')# 'first_name', 'last_name')
    extra_kwargs = {
      # 'first_name': {'required': False},
      # 'last_name': {'required': False}
    }#111abcdefgh
  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs
  def create(self, validated_data):
    print(type(validated_data))
   
    user = User.objects.create(
      username=validated_data['username'],
      email=validated_data['email'],
      # first_name = validated_data['first_name'],
      # last_name=validated_data['last_name']     
    )
    user.set_password(validated_data['password'])
    user.save()  
    return user
  

class VideoSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Video       
        fields = '__all__'          
   

    def create(self, validated_data):     
       return Video.objects.create(**validated_data)

class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serie
        fields = '__all__'

    def create(self, validated_data):
        return Serie.objects.create(**validated_data)
      
      
class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = '__all__'

    def create(self, validated_data):
        return Episode.objects.create(**validated_data)
      
  
class UserFilmEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFilmEvaluation
        fields = '__all__'

    def create(self, validated_data):
        return UserFilmEvaluation.objects.create(**validated_data)
      
class UserSeriesEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSerieEvaluation
        fields = '__all__'

    def create(self, validated_data):
        return UserSerieEvaluation.objects.create(**validated_data)
      

class MyListeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyListe
        fields = '__all__'

    def create(self, validated_data):
        return MyListe.objects.create(**validated_data)  
      
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        return Category.objects.create(**validated_data)  
      
      
class CategoryListSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryListSeries
        fields = '__all__'

    def create(self, validated_data):
        return CategoryListSeries.objects.create(**validated_data)  

class CategoryListFilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryListFilm
        fields = '__all__'

    def create(self, validated_data):
        return CategoryListFilm.objects.create(**validated_data)  
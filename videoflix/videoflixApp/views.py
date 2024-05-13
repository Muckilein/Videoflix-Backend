from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from .serializers import RegisterSerializer,VideoSerializer,EpisodeSerializer,SerieSerializer
from .models import User,Video,Episode,Serie
from .methods import *
# from . methods import *
# Create your views here.
class LoginView(ObtainAuthToken): 
   def post(self, request, *args, **kwargs):       
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})       
        serializer.is_valid(raise_exception=True)       
        user = serializer.validated_data['user']             
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
class RegisterView(generics.CreateAPIView):
    """
    Registers a User when the given data are correct
    """
    queryset = User.objects.all()
    permission_classes = []
    serializer_class = RegisterSerializer
    
class videoClipView(APIView):
    serializer_class = VideoSerializer

    def get(self, request, format=None):
        queryset = Video.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        #serializer = self.serializer_class(queryset[0], many=False)        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        jsondata = request.data
        serializer = self.serializer_class(data=jsondata)
        if serializer.is_valid(raise_exception=True):
             serializer.save()
             msg = {'msg':'Add Clip'}
             return Response(msg, status=status.HTTP_201_CREATED)
    

class EpisodeClipView(APIView):
    serializer_class = EpisodeSerializer

    def get(self, request, format=None):
        queryset = Episode.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        #serializer = self.serializer_class(queryset[0], many=False)        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        jsondata = request.data
        serializer = self.serializer_class(data=jsondata)
        if serializer.is_valid(raise_exception=True):
             serializer.save()
             msg = {'msg':'Add Clip'}
             return Response(msg, status=status.HTTP_201_CREATED)
 
          
class SerieView(APIView):
    serializer_class = SerieSerializer 
   

    def get(self, request, format=None):
        queryset = Serie.objects.all()                
        serializer = self.serializer_class(queryset, many=True)      
        #serializer.data[0] = createEpisodeList(serializer.data[0])
        createEpisodeListAll(serializer.data)             
        return Response(serializer.data, status=status.HTTP_200_OK)

    
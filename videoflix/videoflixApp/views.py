from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer,VideoSerializer,EpisodeSerializer,SerieSerializer,UserFilmEvaluationSerializer,UserSeriesEvaluationSerializer
from .models import User,Video,Episode,Serie,UserFilmEvaluation,UserSerieEvaluation
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
    
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated] 
    
    serializer_class = VideoSerializer

    def get(self, request, format=None):
        queryset = Video.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        data = getEvaluationsFilms(serializer.data, request.user) 
        print(data)             
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        jsondata = request.data
        serializer = self.serializer_class(data=jsondata)
        if serializer.is_valid(raise_exception=True):
             serializer.save()
             msg = {'msg':'Add Clip'}
             return Response(msg, status=status.HTTP_201_CREATED)
 
def getEvaluated(data, keyword):
    list=[]
    for d in data:
        ev = {"vID":d[keyword], "evaluation":d['evaluation']}
        list.append(ev)  
    return list;
       

def getEvaluationsFilms(videoData, currentUser):
    
    filmEvaluation = UserFilmEvaluation.objects.filter(user=currentUser)
    serilizer = UserFilmEvaluationSerializer(filmEvaluation, many = True);   
    list = getEvaluated(serilizer.data,'video')   
    for v in videoData:
        setEvaluation(v, list)
    return videoData

def getEvaluationsSeries(videoData, currentUser):
    
    filmEvaluation = UserSerieEvaluation.objects.filter(user=currentUser)
    serilizer = UserSeriesEvaluationSerializer(filmEvaluation, many = True);   
    list = getEvaluated(serilizer.data,'serie')   
    for v in videoData:
        setEvaluation(v, list)
    return videoData
    
def setEvaluation(vData,evalList):
    for e in evalList:
        if vData['id']== e['vID']:
            vData['evaluation']= e['evaluation']
            break
    
        
    

class EpisodeClipView(APIView):
    serializer_class = EpisodeSerializer

    def get(self, request, format=None):
        queryset = Episode.objects.all()
        serializer = self.serializer_class(queryset, many=True)             
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
        createEpisodeListAll(serializer.data) 
        data = getEvaluationsSeries(serializer.data, request.user) 
        print(data)             
        return Response(data, status=status.HTTP_200_OK)            
       
    
class videoEvaluation(generics.CreateAPIView): 
    
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]   
    
    def get(self, request, format=None):
        current_user = request.user        
        allEval = UserFilmEvaluation.objects.filter(user = current_user)
        allEvalUser= UserFilmEvaluationSerializer(allEval,many=True)        
        return Response(allEvalUser.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data       
        eval = data['eval']
        videoId = data['filmId']
        current_user = request.user      
        video = Video.objects.filter(id = videoId)[0]        
        evaluation = UserFilmEvaluation.objects.create(user=current_user,video = video,evaluation = eval)
        allEval = UserFilmEvaluation.objects.filter(user = current_user)
        allEvalUser= UserFilmEvaluationSerializer(allEval,many=True)
        return Response(allEvalUser.data, status=status.HTTP_200_OK)
    def put(self, request, format=None):
        data = request.data        
        eval = data['eval']
        videoId = data['filmId']
        current_user = request.user       
        video = Video.objects.filter(id = videoId)[0]              
        evaluation = UserFilmEvaluation.objects.filter(user = current_user, video = video)[0] 
        evaluation.evaluation = eval
        evaluation.save()         
        return Response('OK')
    
class serieEvaluation(generics.CreateAPIView): 
    
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]   
    
    def get(self, request, format=None):
        current_user = request.user        
        allEval = UserSerieEvaluation.objects.filter(user = current_user)
        allEvalUser= UserSeriesEvaluationSerializer(allEval,many=True)        
        return Response(allEvalUser.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data        
        eval = data['eval']
        videoId = data['filmId']
        current_user = request.user       
        serie = Serie.objects.filter(id = videoId)[0]       
        evaluation = UserSerieEvaluation.objects.create(user=current_user,serie = serie,evaluation = eval)
        # allEval = UserSerieEvaluation.objects.filter(user = current_user)
        # allEvalUser= UserSeriesEvaluationSerializer(allEval,many=True)
        #return Response(allEvalUser.data, status=status.HTTP_200_OK)
        return Response('OK')
    
    def put(self, request, format=None):
        data = request.data        
        eval = data['eval']
        videoId = data['filmId']
        current_user = request.user       
        serie = Serie.objects.filter(id = videoId)[0]              
        evaluation = UserSerieEvaluation.objects.filter(user = current_user, serie = serie)[0] 
        evaluation.evaluation = eval
        evaluation.save()         
        return Response('OK')
      

    
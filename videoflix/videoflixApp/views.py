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
from .serializers import CategoryListFilmSerializer,CategoryListSeriesSerializer,RegisterSerializer,VideoSerializer,EpisodeSerializer,SerieSerializer,UserFilmEvaluationSerializer,UserSeriesEvaluationSerializer,MyListeSerializer,CategorySerializer
from .models import User,Video,Episode,Serie,UserFilmEvaluation,UserSerieEvaluation,MyListe,Category,CategoryListSeries,CategoryListFilm
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
        data = adjustFilm(serializer.data, request.user,'Film') 
        #getInList(data,request.user,'Film')             
        return Response(data, status=status.HTTP_200_OK)

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
        data = adjustSerie(serializer.data, request.user,'Serie')         
        # getInList(data,request.user,'Serie')          
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
    
def getIdListFromCategory(data):
    idList = []    
    for elem in data:
        idList.append(elem['video'])    
    return idList
    
class categoryItemDetail(APIView):
  
    # authentication_classes =[TokenAuthentication]
    # permission_classes =[IsAuthenticated]
    
    def get(self,request,pk):  #self ist wichtig
        cat = Category.objects.filter(id = pk)[0]
        s=CategoryListSeries.objects.filter(category = cat)
        f=CategoryListFilm.objects.filter(category = cat)
        current_user=request.user
        filmSer=CategoryListFilmSerializer(s, many=True).data
        serSer=CategoryListSeriesSerializer(f, many=True).data
        print(filmSer)
        print(serSer)
        filmSerID=getIdListFromCategory(filmSer)
        serSerID=getIdListFromCategory(serSer)
        print(filmSerID)
        print(serSerID)
        serie = getSerie(serSerID,current_user)  
        film = getFilms(filmSerID,current_user)     
   
        return Response(film+serie, status=status.HTTP_200_OK)
    
        
        #   queryset = Video.objects.all()
        # serializer = self.serializer_class(queryset, many=True)
        # data = adjustFilm(serializer.data, request.user,'Film') 
        #getInList(data,request.user,'Film')             
        
    
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
    
    
 
    
class getMyList(generics.CreateAPIView):     
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]   
    
    def get(self, request, format=None):
        current_user = request.user        
        myListSeries = MyListe.objects.filter(user = current_user, type = "Serie")
        myListFilm = MyListe.objects.filter(user = current_user, type = "Film")
        listDataSerie= MyListeSerializer(myListSeries,many=True).data 
        listDataFilm= MyListeSerializer(myListFilm,many=True).data 
        idListFilm= makeListData(listDataFilm)
        idListSerie= makeListData(listDataSerie)
        print('listDataFilm')
        print(listDataFilm)
        serie = getSerie(idListSerie,current_user)  
        film = getFilms(idListFilm,current_user)      
        return Response(film+serie, status=status.HTTP_200_OK)

    def post(self, request, format=None): 
        type = request.data['type']
        idofObject = request.data['idObject'] 
        user= request.user 
        inListObject = MyListe.objects.create(user=user,type = type,idObject=idofObject)
        print(inListObject)
        return Response('OK')
    
    def delete(self, request, format=None):
        type = request.data['type']
        idofObject = request.data['idObject']
        user= request.user
        object = MyListe.objects.filter(user=user,type = type,idObject=idofObject)
        object.delete()
        return Response('OK')
      

class getCategory(generics.CreateAPIView):     
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]   
    
    def get(self, request, format=None):
        current_user = request.user  
        category = Category.objects.all();      
        dataCat = CategorySerializer(category,many=True).data      
        return Response(dataCat, status=status.HTTP_200_OK)

   
      
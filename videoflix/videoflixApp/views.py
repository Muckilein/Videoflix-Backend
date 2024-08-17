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
from .serializers import EmailVerificationSerializer,CategoryListFilmSerializer,CategoryListSeriesSerializer,RegisterSerializer,VideoSerializer,EpisodeSerializer,SerieSerializer,UserFilmEvaluationSerializer,UserSeriesEvaluationSerializer,MyListeSerializer,CategorySerializer
from .models import User,Video,Episode,Serie,UserFilmEvaluation,UserSerieEvaluation,MyListe,Category,CategoryListSeries,CategoryListFilm
from .methods import *
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import  GenericAPIView
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class LoginView(ObtainAuthToken): 
    """
    Login  
       
    """
    def post(self, request, *args, **kwargs):       
        serializer = self.serializer_class(data=request.data, context={'request': request})  
                  
        try:
            serializer.is_valid(raise_exception=True)       
            user = serializer.validated_data['user']           
            if(user.is_verified):           
             token, created = Token.objects.get_or_create(user=user)
             return Response({
                'status':'ok',
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
                 })
            else:
                return Response({'status': 'Account not yet verified'}, status=status.HTTP_401_UNAUTHORIZED)
        except AuthenticationFailed:
            return Response({'status': 'error'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:           
            return Response({'status': 'error', 'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        

class LogoutView(APIView):
    """
    Loggout of the logged in user
    """   
    def get(self,request,format=None):
        logout(request)
        return Response("Logged Out") 
        
class RegisterView(generics.CreateAPIView):
    """
    Registers a User when the given data are correct
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []
    
    
    def post(self, request):
     serializer = self.get_serializer(data=request.data)
     serializer.is_valid(raise_exception=True)
     user = serializer.save()       
     dataRequest = request.data
           
    # getting tokens
     user_email = User.objects.get(email=dataRequest['email'])
     tokens = RefreshToken.for_user(user_email).access_token
        # send email for user verification
     current_site = get_current_site(request).domain
     relative_link = reverse('email-verify')
     absurl = 'http://'+current_site+relative_link+"?token="+str(tokens)
     email_body = 'Hi '+dataRequest['username'] + \
            ' Use the link below to verify your email \n' + absurl
     data = {'email_body': email_body, 'to_email': dataRequest['email'],
                'email_subject': 'Verify your email'}

     Util.send_email(data=data) 
     return Response({'user_data': dataRequest, 'access_token' : str(tokens)}, status=status.HTTP_201_CREATED)
    
 
 
class VerifyEmail(GenericAPIView ):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            print(payload)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
   

    
class videoClipView(APIView):
    
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]     
    serializer_class = VideoSerializer

    def get(self, request, format=None):
        queryset = Video.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        data = adjustFilm(serializer.data, request.user)                     
        return Response(data, status=status.HTTP_200_OK)
               

class EpisodeClipView(APIView):
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated] 
    
    serializer_class = EpisodeSerializer

    def get(self, request, format=None):
        queryset = Episode.objects.all()
        serializer = self.serializer_class(queryset, many=True)             
        return Response(serializer.data, status=status.HTTP_200_OK)    
   
        
class SerieView(APIView):
    serializer_class = SerieSerializer
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]  

    def get(self, request, format=None):
        queryset = Serie.objects.all()                
        serializer = self.serializer_class(queryset, many=True)  
        data = adjustSerie(serializer.data, request.user)       
        return Response(data, status=status.HTTP_200_OK)            
       
    
class videoEvaluation(generics.CreateAPIView): 
    """
    Return, creates or changes the evalutaion value for all videos
    """
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
        video = Video.objects.filter(id = videoId)
        if len(video)>0: 
            video = video[0]                  
            evaluation = UserFilmEvaluation.objects.create(user=current_user,video = video,evaluation = eval)
            allEval = UserFilmEvaluation.objects.filter(user = current_user)
            allEvalUser= UserFilmEvaluationSerializer(allEval,many=True)
            return Response(allEvalUser.data, status=status.HTTP_200_OK)
        else:
            return Response({'status':'error'}, status=status.HTTP_404_NOT_FOUND)
            
    def put(self, request, format=None):
        data = request.data        
        eval = data['eval']
        videoId = data['filmId']
        current_user = request.user       
        video = Video.objects.filter(id = videoId)[0]             
        evaluation = UserFilmEvaluation.objects.filter(user = current_user, video = video)
        if len(evaluation)>0: 
            evaluation=evaluation[0]           
            evaluation.evaluation = eval
            evaluation.save()         
            return Response('OK')
        else:
            return Response({'status':'error'}, status.HTTP_404_NOT_FOUND)
            
    

    
class categoryItemDetail(APIView):
    """
    get: returns the JSON with all information of all series of films with the given category
    """
  
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]
    
    def get(self,request,pk):  #self ist wichtig
        cat = Category.objects.filter(id = pk)[0]
        current_user = request.user
        # get all Series data
        s=CategoryListSeries.objects.filter(category = cat)
        serSer=CategoryListSeriesSerializer(s, many=True).data 
        serSerID=getIdListFromCategory(serSer)      
        serie = getSerie(serSerID,current_user)   
        # get all Series data   
        f=CategoryListFilm.objects.filter(category = cat)
        current_user=request.user
        filmSer=CategoryListFilmSerializer(f, many=True).data       
        filmSerID=getIdListFromCategory(filmSer)       
        film = getFilms(filmSerID,current_user)     
   
        return Response(film+serie, status=status.HTTP_200_OK)         
                    
    
class serieEvaluation(generics.CreateAPIView): 
    """
    Return, creates or changes the evalutaion value for all serien
    """
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
        serie = Serie.objects.filter(id = videoId) 
        if len(serie)>0: 
            serie=serie[0]     
            evaluation = UserSerieEvaluation.objects.create(user=current_user,serie = serie,evaluation = eval) 
            return Response('OK')       
            
    
    def put(self, request, format=None):
        data = request.data        
        eval = data['eval']
        videoId = data['filmId']
        current_user = request.user       
        serie = Serie.objects.filter(id = videoId)[0]                      
        evaluation = UserSerieEvaluation.objects.filter(user = current_user, serie = serie) 
        if len(evaluation)>0:
         evaluation=evaluation[0] 
         evaluation.evaluation = eval
         evaluation.save()         
         return Response('OK')
        else:
            return Response({'status':'error'}, status.HTTP_404_NOT_FOUND)  
    
 
    
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
        category = Category.objects.all();      
        dataCat = CategorySerializer(category,many=True).data      
        return Response(dataCat, status=status.HTTP_200_OK)

   
      
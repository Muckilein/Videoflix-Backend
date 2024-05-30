from .serializers import EpisodeSerializer,VideoSerializer,UserFilmEvaluationSerializer,SerieSerializer,UserSeriesEvaluationSerializer,CategorySerializer,MyListeSerializer
from .models import Episode,Video,UserFilmEvaluation,Serie,UserSerieEvaluation,Category,MyListe

def createEpisodeList(serializedData):
    #Auslagern in methodes.py und für alle und nicht nur für [0]
    serializer_Episodes = EpisodeSerializer  
      
    episodeList =serializedData['episodeList']
    querysetEpisodes = Episode.objects.filter(id__in=episodeList)  
    serializedEpisodes = serializer_Episodes(querysetEpisodes, many=True)    
    serializedData['episodeList'] = serializedEpisodes.data  
    return serializedData  
  
         
def updateData(d,listData):   
        for ld in listData:
            if ld['idObject']== d['id']:
                d['inList']=True
                
def getEvaluated(data, keyword):
    list=[]
    for d in data:
        ev = {"vID":d[keyword], "evaluation":d['evaluation']}
        list.append(ev)  
    return list;

def setEvaluation(vData,evalList):
    for e in evalList:
        if vData['id']== e['vID']:
            vData['evaluation']= e['evaluation']
            break

def setCat(vDataCat,catData):
   
     list =[]
     for vC in vDataCat:
          for c in catData:
              if vC == c['id']:
                   list.append(c)               
     return list                 
          
      
def adjustFilm(videoData, currentUser,t):
    cat = Category.objects.all()
    categoryData = CategorySerializer(cat,many=True).data 
    
    listSerialister = MyListeSerializer
    list = MyListe.objects.filter(user=currentUser,type=t)
    listData = listSerialister(list,many=True).data
    
    filmEvaluation = UserFilmEvaluation.objects.filter(user=currentUser)
    serilizer = UserFilmEvaluationSerializer(filmEvaluation, many = True);   
    list = getEvaluated(serilizer.data,'video')   
    for v in videoData:
        updateData(v,listData)
        setEvaluation(v, list)
        v['category'] = setCat(v['category'],categoryData) 
    return videoData 

def adjustSerie(videoData, currentUser,t):
    cat = Category.objects.all()
    categoryData = CategorySerializer(cat,many=True).data
    
    listSerialister = MyListeSerializer
    list = MyListe.objects.filter(user=currentUser,type=t)
    listData = listSerialister(list,many=True).data 
     
    
    seriesEvaluation = UserSerieEvaluation.objects.filter(user=currentUser)
    serilizer = UserSeriesEvaluationSerializer(seriesEvaluation, many = True);   
    list = getEvaluated(serilizer.data,'serie')   
    for v in videoData:
        updateData(v,listData)
        createEpisodeList(v)
        setEvaluation(v, list)
        v['category'] = setCat(v['category'],categoryData)        
    return videoData            
                
def makeListData(data):
    idList = []    
    for elem in data:
        idList.append(elem['idObject'])    
    return idList

def getFilms(data,user):
      videoSerielizer = VideoSerializer     
      queryset = Video.objects.filter(pk__in=data)
      serializer = videoSerielizer(queryset, many=True)
      dataFilm = adjustFilm(serializer.data, user,'Film') 
      return dataFilm 
  
def getSerie(data,user):
        serieSerializer = SerieSerializer         
        queryset = Serie.objects.filter(pk__in=data)                
        serializer = serieSerializer(queryset, many=True)  
        data = adjustSerie(serializer.data,user,'Serie') 
        return data
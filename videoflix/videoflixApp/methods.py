from .serializers import EpisodeSerializer,VideoSerializer,UserFilmEvaluationSerializer,SerieSerializer,UserSeriesEvaluationSerializer,CategorySerializer
from .models import Episode,Video,UserFilmEvaluation,Serie,UserSerieEvaluation,Category

def createEpisodeList(serializedData):
      #Auslagern in methodes.py und für alle und nicht nur für [0]
    serializer_Episodes = EpisodeSerializer  
      
    episodeList =serializedData['episodeList']
    querysetEpisodes = Episode.objects.filter(id__in=episodeList)  
    serializedEpisodes = serializer_Episodes(querysetEpisodes, many=True)    
    serializedData['episodeList'] = serializedEpisodes.data  
    return serializedData  

  

def createEpisodeListAll(serializedData):
    for series in serializedData:
        series = createEpisodeList(series) 
        
         
def updateData(data,listData):
    for d in data:
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
    #  print(vDataCat)
    #  print(catData)
     list =[]
     for vC in vDataCat:
          for c in catData:
              if vC == c['id']:
                   list.append(c)
    #  print(list)            
     return list                    
           

       

def adjustFilm(videoData, currentUser):
    cat = Category.objects.all()
    categoryData = CategorySerializer(cat,many=True).data 
    
    filmEvaluation = UserFilmEvaluation.objects.filter(user=currentUser)
    serilizer = UserFilmEvaluationSerializer(filmEvaluation, many = True);   
    list = getEvaluated(serilizer.data,'video')   
    for v in videoData:
        setEvaluation(v, list)
        v['category'] = setCat(v['category'],categoryData) 
    return videoData 

def adjustSerie(videoData, currentUser):
    cat = Category.objects.all()
    categoryData = CategorySerializer(cat,many=True).data 
    
    seriesEvaluation = UserSerieEvaluation.objects.filter(user=currentUser)
    serilizer = UserSeriesEvaluationSerializer(seriesEvaluation, many = True);   
    list = getEvaluated(serilizer.data,'serie')   
    for v in videoData:
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
      list = makeListData(data)
      print(list)
      queryset = Video.objects.filter(pk__in=list)
      serializer = videoSerielizer(queryset, many=True)
      dataFilm = adjustFilm(serializer.data, user) 
      return dataFilm 
  
def getSerie(data,user):
        serieSerializer = SerieSerializer  
        list = makeListData(data)
        queryset = Serie.objects.filter(pk__in=list)                
        serializer = serieSerializer(queryset, many=True)     
        createEpisodeListAll(serializer.data) 
        data = adjustSerie(serializer.data,user) 
        return data
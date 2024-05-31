from .serializers import EpisodeSerializer,VideoSerializer,UserFilmEvaluationSerializer,SerieSerializer,UserSeriesEvaluationSerializer,CategorySerializer,MyListeSerializer
from .models import Episode,Video,UserFilmEvaluation,Serie,UserSerieEvaluation,Category,MyListe

def createEpisodeList(serializedData):
    """
     Args:
         serializedData (JSON) :JSON data of a serie
     Returns:
        JSON : Input with adjusted episode list
    """  
    serializer_Episodes = EpisodeSerializer  
      
    episodeList =serializedData['episodeList']
    querysetEpisodes = Episode.objects.filter(id__in=episodeList)  
    serializedEpisodes = serializer_Episodes(querysetEpisodes, many=True)    
    serializedData['episodeList'] = serializedEpisodes.data  
    return serializedData  
  
         
def updateData(d,listData): 
    """
    Adjust the 'inList' Value of a series or film
    Args:
        d (JSON): JSON with all the data of a film or series
        listData (JSON Array): e.g. [{'id': 13, 'type': 'Serie', 'idObject': 2, 'user': 2}]
    Returns:
        JSON : JSON with all the data of a film or series with Adjusted  'inList' value
    """ 
    print(listData)
    for ld in listData:
            if ld['idObject']== d['id']:
                d['inList']=True
                
def getEvaluated(data, keyword):
    """Adds the korrect evaluation to the JSON data of a film or series
    Args:
        data (JSON Array): JSON Array with all the film or series data
        keyword (string): 'video' or 'series'
    Returns:
        JSON Array: [{"vID":1, "evaluation":2},....]
    """
    list=[]      
    for d in data:               
        ev = {"vID":d[keyword], "evaluation":d['evaluation']}
        list.append(ev)  
    
    return list;

def setEvaluation(vData,evalList):
    """Sets the korrect evalulation Value in vData
    Args:
        vData (JSON): JSON data of a film or series
        evalList (JSON Array): [{'vID': 2, 'evaluation': 0}]
    """   
    for e in evalList:      
        if vData['id']== e['vID']:
            vData['evaluation']= e['evaluation']
            break

def setCat(vDataCat,catData):
     """Sets the data of
     Args:
        vDataCat (Array): raw category data of a  serie or film [1,2,3]. Numbers are the id`s of the categories
        catData (_type_): category information from database 'Category'.
     Returns:
        List in which the id of a category is replaced by the detialed iinformation from the Category database.
        from [1,2,3] to [{"id"=1,"name":....},{"id"=2,"name":....},...]
     """
     list =[]
     for vC in vDataCat:
          for c in catData:
              if vC == c['id']:
                   list.append(c)               
     return list                 
          
      
def adjustFilm(videoData, currentUser):
    """ Extract all nessesary inforamtion from the other database and adjust the given filmt data.
    Args:
        videoData (JSON Array): Raw film data that is directly extracted from the database
        currentUser (User): logged in User    
    Returns:
       A JSON array with all informations about the series combines form all databases
    """
    cat = Category.objects.all()
    categoryData = CategorySerializer(cat,many=True).data 
    
    listSerialister = MyListeSerializer
    list = MyListe.objects.filter(user=currentUser,type='Film')
    listData = listSerialister(list,many=True).data
    
    filmEvaluation = UserFilmEvaluation.objects.filter(user=currentUser)
    serilizer = UserFilmEvaluationSerializer(filmEvaluation, many = True);   
    listEval = getEvaluated(serilizer.data,'video')   
    for v in videoData:
        updateData(v,listData)
        setEvaluation(v, listEval)
        v['category'] = setCat(v['category'],categoryData) 
    return videoData 

def adjustSerie(videoData, currentUser):
    """ Extract all nessesary inforamtion from the other database and adjust the given series data.
    Args:
        videoData (JSON Array): Raw series data that is directly extracted from the database
        currentUser (User): logged in User   
    Returns:
       A JSON array with all informations about the series combines form all databases
    """
    cat = Category.objects.all()
    categoryData = CategorySerializer(cat,many=True).data
    
    listSerialister = MyListeSerializer
    list = MyListe.objects.filter(user=currentUser,type='Serie')
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
    """      
    Args:
        data(JSON Array):[{"user":idU,"type":"Serie","idObject":idO},...]
    Returns:
         [idO,...]
    """
    idList = []    
    for elem in data:
        idList.append(elem['idObject'])    
    return idList

def getIdListFromCategory(data):
    """
    Gets a Json Array in Form [{"category":idC,"video":idV},...] and returns [idV,...]
    """
    idList = []    
    for elem in data:
        idList.append(elem['video'])    
    return idList

def getFilms(data,user):
      """
      Returns all films (with all informations) that have their id in data.
      data:[idfilm,....]
      """
      videoSerielizer = VideoSerializer     
      queryset = Video.objects.filter(pk__in=data)
      serializer = videoSerielizer(queryset, many=True)
      dataFilm = adjustFilm(serializer.data, user) 
      return dataFilm 
  
def getSerie(data,user):
        """
        Returns all series (with all informations) that have their id in data.
        data:[idseries,....]
        """
        serieSerializer = SerieSerializer         
        queryset = Serie.objects.filter(pk__in=data)                
        serializer = serieSerializer(queryset, many=True)  
        data = adjustSerie(serializer.data,user) 
        return data
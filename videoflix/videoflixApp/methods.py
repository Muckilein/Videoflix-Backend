from .serializers import EpisodeSerializer
from .models import Episode

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
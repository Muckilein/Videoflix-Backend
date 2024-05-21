from django.contrib import admin
from .models import User,Video,Episode,Serie,Category,CategoryListFilm,CategoryListSeries,EpisodeList,UserSerieEvaluation,UserFilmEvaluation,MyListe
#from import_export import resources

@admin.register(User)
class UserAdmin(admin.ModelAdmin): 
    fields = ( 'email' , 'username','first_name','last_name')    
    list_display = ('email' , 'username','first_name','last_name',)    
    search_fields = ('username',)
    
@admin.register (Video)
class VideoAdmin(admin.ModelAdmin): 
     fields = ('title','created_at','description','video_file','genre','type','fsk','short_file','img','evaluation','inList') # nitice category is a many-to-many field and not shown here
     list_display = ('title','created_at','description','video_file','genre','type','fsk','short_file','img','evaluation','inList')    
     search_fields = ('title',)
     
     
@admin.register (Episode)
class EpisodeAdmin(admin.ModelAdmin): 
     fields = ('title','created_at','description','video_file','img','season','episode')  
     list_display = ('title','created_at','description','video_file','img','season','episode')    
     search_fields = ('title',)

@admin.register (Category)
class CategoryAdmin(admin.ModelAdmin): 
     fields = ('name',)  
     list_display = ('name',)    
     search_fields = ('name',)
       
@admin.register (Serie)
class SeriesAdmin(admin.ModelAdmin): 
     fields =  ('title','description','genre','img','short_file','type','numSeasons','evaluation','inList')  
     list_display = ('title','description','genre','img','short_file','type','numSeasons','evaluation','inList')    
     search_fields = ('title',)      
     

     
@admin.register (CategoryListFilm)
class CategoryListFilmAdmin(admin.ModelAdmin): 
     fields = ('category','video')  
     list_display = ('category','video')    
     search_fields = ('category',)
     
@admin.register (CategoryListSeries)
class CategoryListSeriesAdmin(admin.ModelAdmin): 
     fields = ('category','video')  
     list_display = ('category','video')    
     search_fields = ('category',)
     
@admin.register (EpisodeList)
class EpisodeListsAdmin(admin.ModelAdmin): 
     fields = ('episode','series')  
     list_display = ('episode','series')    
     search_fields = ('episode',)
     
     
@admin.register (UserSerieEvaluation)
class UserSerieEvaluationsAdmin(admin.ModelAdmin): 
     fields = ('user','serie','evaluation')  
     list_display = ('user','serie','evaluation')    
     search_fields = ('user',)

@admin.register (UserFilmEvaluation)
class UserFilmEvaluationAdmin(admin.ModelAdmin): 
     fields = ('user','video','evaluation')  
     list_display = ('user','video','evaluation')    
     search_fields = ('user',)
     
@admin.register (MyListe)
class MyListeAdmin(admin.ModelAdmin): 
     fields = ('user','type','idObject')  
     list_display = ('user','type','idObject')    
     search_fields = ('user',)
          

     
# class VideoResource(resources.ModelResource):

#     class Meta:
#         model = Video
        
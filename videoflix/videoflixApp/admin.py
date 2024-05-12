from django.contrib import admin
from .models import User,Video,Episode,Serie,Category,CategoryListFilm,CategoryListSeries,EpisodeList
#from import_export import resources

@admin.register(User)
class UserAdmin(admin.ModelAdmin): 
    fields = ( 'email' , 'username','first_name','last_name')    
    list_display = ('email' , 'username','first_name','last_name',)    
    search_fields = ('username',)
    
@admin.register (Video)
class VideoAdmin(admin.ModelAdmin): 
     fields = ('title','created_at','description','video_file','genre','type','fsk','short_file','img') # nitice category is a many-to-many field and not shown here
     list_display = ('title','created_at','description','video_file','genre','type','fsk','short_file','img')    
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
     fields =  ('title','description','genre','img','short_file','type','numSeasons')  
     list_display = ('title','description','genre','img','short_file','type','numSeasons')    
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
     
     
     
# class VideoResource(resources.ModelResource):

#     class Meta:
#         model = Video
        
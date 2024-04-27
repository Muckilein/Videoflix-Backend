from django.contrib import admin
from .models import User,Video
#from import_export import resources

@admin.register(User)
class UserAdmin(admin.ModelAdmin): 
    fields = ( 'email' , 'username','first_name','last_name')    
    list_display = ('email' , 'username','first_name','last_name',)    
    search_fields = ('username',)
    
@admin.register (Video)
class VideoAdmin(admin.ModelAdmin): 
     fields = ('title','created_at','description','video_file','genre','type','fsk')  
     list_display = ('title','created_at','description','video_file','genre','type','fsk')    
     search_fields = ('title',)
     
# class VideoResource(resources.ModelResource):

#     class Meta:
#         model = Video
        
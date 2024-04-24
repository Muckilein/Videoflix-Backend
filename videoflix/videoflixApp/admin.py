from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin): 
    fields = ( 'email' , 'username','first_name','last_name')    
    list_display = ('email' , 'username','first_name','last_name',)    
    search_fields = ('username',)

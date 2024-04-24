from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin): 
    fields = ( 'email' , 'username', 'short')    
    list_display = ('email' , 'username', 'short')    
    search_fields = ('username',)

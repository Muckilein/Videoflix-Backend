from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from datetime import date
from django.core.mail import EmailMessage
import threading



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_superuser(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)

    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError('Superuser must have is_staff=True.')
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')

    #     return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
     email=models.CharField(max_length=100,unique=True)   
     username=models.CharField(max_length=100,default=' ')    
     first_name=models.CharField(max_length=100,default=' ')
     last_name=models.CharField(max_length=100,default=' ')
     is_verified = models.BooleanField(default=False)
    
     USERNAME_FIELD = "email"
     REQUIRED_FIELDS = []
     objects = CustomUserManager() 
     def __str__(self):        
        return  self.username 
    
class Category(models.Model):
    name=models.CharField(max_length=50,unique=True)
    
    def __str__(self):
       return  (self.name)
   
    
class Video(models.Model):
     title=models.CharField(max_length=100,unique=True)
     description = models.CharField(max_length=500)   
     genre=models.CharField(max_length=100,default=' ')    
     type=models.CharField(max_length=100,default=' ')
     fsk=models.CharField(max_length=100,default=' ')
     created_at = models.DateField(default=date.today)    
     video_file = models.FileField(upload_to='videos', blank=True, null=True)
     short_file = models.FileField(upload_to='short', blank=True, null=True)
     img = models.ImageField(upload_to='bilder/',blank=True, null=True)
     category=  models.ManyToManyField(Category,through='CategoryListFilm')
     evaluation=models.IntegerField(default=-1,null=True)
     inList = models.BooleanField(default=False)  
     
     def __str__(self):
       return  (self.title)   

class CategoryListFilm(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    video= models.ForeignKey(Video, on_delete=models.CASCADE) 
    
    def __str__(self):
       return  (self.category.name + " " +self.video.title) 

   
class Episode(models.Model):
    title=models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=500)   
    created_at = models.DateField(default=date.today)    
    video_file = models.FileField(upload_to='Episodes', blank=True, null=True)  
    season = models.IntegerField(default=1)
    episode = models.IntegerField(default=1)   
    img = models.ImageField(upload_to='bilder/',blank=True, null=True) 
   # serie= models.ForeignKey(Serie, on_delete=models.CASCADE,null=True) Series ans Episode is actualy a one to many relationsship, but I decided to make a ManyToManyFiel in Series

    def __str__(self):
       return  (self.title) 
     

class Serie(models.Model):
     title=models.CharField(max_length=100,unique=True)
     description = models.CharField(max_length=500)
     type=models.CharField(max_length=100,default=' ')   
     genre=models.CharField(max_length=100,default=' ')    
     short_file = models.FileField(upload_to='short', blank=True, null=True)
     img = models.ImageField(upload_to='bilder/',blank=True, null=True) 
     category=  models.ManyToManyField(Category,through='CategoryListSeries')
     numSeasons = models.IntegerField()
     episodeList = models.ManyToManyField(Episode,through='EpisodeList')
     evaluation=models.IntegerField(default=-1,null=True)
     inList = models.BooleanField(default=False)    
     
     
     def __str__(self):
       return  self.title 
 

class MyListe(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE) 
    type = models.CharField(max_length=100) 
    idObject=models.IntegerField()
    
    def __str__(self):
       return  self.user.username + " " + self.type  

class UserSerieEvaluation(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    serie=models.ForeignKey(Serie, on_delete=models.CASCADE)
    evaluation = models.IntegerField(null=True)
    
    def __str__(self):
       return  (self.user.username + " " +self.serie.title ) 
   
class UserFilmEvaluation(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    video=models.ForeignKey(Video, on_delete=models.CASCADE)
    evaluation = models.IntegerField(null=True)
    
    def __str__(self):
       return  (self.user.username + " " +self.video.title )
 
# delete later    
class EpisodeList(models.Model):
    episode=models.ForeignKey(Episode, on_delete=models.CASCADE)
    series= models.ForeignKey(Serie, on_delete=models.CASCADE)   
          
    def __str__(self):
       return  (self.episode.title + " " +self.series.title) 
   
    

class CategoryListSeries(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    video= models.ForeignKey(Serie, on_delete=models.CASCADE)   
    
  
        
    
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "http://localhost:4200/newPassword?path={}&token={}".format(
          instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
          reset_password_token.key)   
        }
    #  'reset_password_url': "http://127.0.0.1:5500/html/reset-your-password.html?path={}&token={}".format(
    #       instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
    #       reset_password_token.key)   
    #     }
    print(context)

    # render email text 
    email_html_message = render_to_string('user_reset_password.html', context)
    email_plaintext_message = render_to_string('user_reset_password.txt', context)
    print(email_html_message)
    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()   
    


    


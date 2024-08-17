from .models import Video,Episode
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import os
from .tasks import convert_480p,convert_720p,convert_1080p
import django_rq

@receiver(post_save,sender = Video)
def video_post_save(sender,instance, created, **kwargs):
    print('Video wurde gespeichert')
    if created:
        print('new video created')

 #       queue = django_rq.get_queue('default',autocommit=True)
#        queue.enqueue(convert_480p,instance.video_file.path)
        convert_480p(instance.video_file.path) # Funktion siehe in tasks.py
 #       convert_720p(instance.video_file.path) 
  #      convert_1080p(instance.video_file.path) 

        
@receiver(post_delete,sender = Video)
def video_post_delete(sender,instance, **kwargs):   
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            print('Video wurde gelöscht')
            os.remove(instance.video_file.path)
            
            

@receiver(post_save,sender = Episode)
def  episode_post_save(sender,instance, created, **kwargs):
    print('Episode wurde gespeichert')
    if created:
        print('new Episode created')
        #queue = django_rq.get_queue('default',autocommit=True)
        #queue.enqueue(convert_480p,instance.video_file.path)
      #  convert_480p(instance.video_file.path) # Funktion siehe in tasks.py
       # convert_720p(instance.video_file.path)
        #convert_1080p(instance.video_file.path) 
        
@receiver(post_delete,sender = Video)
def episode_post_delete(sender,instance, **kwargs):   
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            print('Episode wurde gelöscht')
            os.remove(instance.video_file.path)

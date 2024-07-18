"""
URL configuration for videoflix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from videoflixApp.views import LogoutView, LoginView,RegisterView,videoClipView,EpisodeClipView,SerieView,videoEvaluation,serieEvaluation,getMyList,getCategory,categoryItemDetail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('registerAPI/', RegisterView.as_view(), name='auth_register'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('__debug__/', include("debug_toolbar.urls")),
    path('videoclip/', videoClipView.as_view()),
    path('episodenclip/', EpisodeClipView.as_view()),
    path('series/', SerieView.as_view()),
    path('videoEvaluation/', videoEvaluation.as_view()),
    path('serieEvaluation/', serieEvaluation.as_view()),
    path('getMyList/', getMyList.as_view()),
    path('getCategory/', getCategory.as_view()),
    path('getItemOfCategory/<int:pk>/', categoryItemDetail.as_view()) ,
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

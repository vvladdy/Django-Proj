
from django.urls import path, include
from .views import index, gallery, singlepost
from . import views

urlpatterns = [
    path('', index, name='index'),
    # path('', views.TitlePagin.as_view(), name='index'),
    # динамическое формирование имени url
    path('singlepost/<slug:slug>/', singlepost, name='singlepost'),
    path('gallery/', views.GallerPhoto.as_view(), name='gallery'),
    #path('contact/', contact, name='contact')
]

# views.GallerPhoto.as_view() для разбивки и вывода нумерации страниц
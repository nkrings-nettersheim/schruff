from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.index, name='index'),
    path('impressum/', views.impressum, name='impressum'),
    path('datenschutz/', views.datenschutz, name='datenschutz'),
    path('step1/', views.step1, name='step1'),
    path('step2/', views.step2, name='step2'),
    path('product1/', views.step2, name='product1'),
    path('product2/', views.step2, name='product2'),
    path('collectiontime/', views.collectiontime, name='collectiontime'),
    path('customer/', views.customer, name='customer'),
    path('complete/', views.complete, name='complete'),
    path('thanks/', views.thanks, name='thanks'),
]

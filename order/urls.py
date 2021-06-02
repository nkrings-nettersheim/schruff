from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.index, name='index'),
    path('impressum/', views.impressum, name='impressum'),
    path('datenschutz/', views.datenschutz, name='datenschutz'),
    path('collectiondate/', views.collectiondate, name='collectiondate'),
    path('product/', views.product, name='product'),
    path('collectiontime/', views.collectiontime, name='collectiontime'),
    path('customer/', views.customer, name='customer'),
    path('complete/', views.complete, name='complete'),
    path('thanks/', views.thanks, name='thanks'),
    path('startfasttrack/', views.start_fasttrack, name='fasttrackstart'),
    path('fasttrack/', views.fasttrack, name='fasttrack'),
    path('fasttracksave/', views.fasttrack_save, name='fasttracksave'),
    path('startorderlist/', views.start_order_list, name='orderliststart'),
    path('orderlist/', views.order_list, name='orderlist'),
]

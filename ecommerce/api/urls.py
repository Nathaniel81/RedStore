from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.apiOverview, name='api-overview'),
 	path('create/', views.itemCreate, name='create'),
	path('list/', views.itemsList, name='list'),
 	path('detail/<str:pk>/', views.itemDetail, name='detail'),
	path('update/<str:pk>/', views.itemUpdate, name='update'),
 	path('delete/<str:pk>/', views.itemDelete, name='delete'),
]
from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('',           views.index,     name='index'),
    path('books/',     views.books,     name='books'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

from django.urls import path, include
from . import views, ajax

urlpatterns = [
    path('', views.doc_list, name="Doc_index"),
    path('add/', views.doc_add, name="Doc_add"),
    path('ajax/getdocnum/', ajax.getdocnum),
]
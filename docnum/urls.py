from django.urls import path, include
from . import views, ajax

urlpatterns = [
    path('', views.doc_list, name="Doc_index"),
    # path('add/', views.doc_add, name="Doc_add"), #舊版新增頁面
    path('add/', views.doc_add_v2, name="Doc_add"),
    path('result/<int:id_docnum>/', views.doc_result, name="Doc_add_result"),
    path('ajax/getdocnum/', ajax.getdocnum),
    path('company/', views.comp_list, name="Comp_index"),
    path('company/<int:comp_id>/', views.comp_detail, name="Comp_detail"),
]
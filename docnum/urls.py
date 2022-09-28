from django.urls import path, include
from . import views, ajax

urlpatterns = [
    path('company/', views.comp_list, name="Comp_index"),
    path('company/<int:comp_id>/', views.comp_detail, name="Comp_detail"),
    path('ajax/getdocnum/', ajax.getdocnum),
    path('send/', views.doc_list, name="Doc_index"),
    path('send/export/', views.send_export, name="Send_Export"),
    path('send/add/', views.doc_add_v2, name="Doc_add"),
    path('send/<int:id_docnum>/', views.doc_result, name="Doc_add_result"),
    path('receive/', views.receivedoc_list, name="Receive_List"),
    path('receive/export/', views.receive_export, name="Receive_Export"),
    path('receive/add/', views.receivedoc_add, name="Receive_add"),
    path('receive/<int:id_rcvdoc>/', views.receivedoc_result, name="Receive_result"),

]
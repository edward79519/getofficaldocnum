from django.urls import path, include
from . import views, ajax

urlpatterns = [
    path('non_auth_error/', views.non_auth_page, name="Non_auth_error"),
    path('company/', views.comp_list, name="Comp_index"),
    path('company/<int:comp_id>/', views.comp_detail, name="Comp_detail"),
    path('company/<int:comp_id>/switch/', views.switch_comp, name="Comp_switch"),
    path('company/<int:comp_id>/delete/', views.comp_del, name="Comp_delete"),
    path('department/', views.dept_list, name="Dept_list"),
    path('departnemt/<int:dept_id>/switch/', views.switch_dept, name="Dept_switch"),
    path('departnemt/<int:dept_id>/delete/', views.dept_del, name="Dept_delete"),
    path('ajax/getdocnum/', ajax.getdocnum),
    path('send/', views.doc_list, name="Doc_index"),
    path('send/export/', views.send_export, name="Send_Export"),
    path('send/add/', views.doc_add_v2, name="Doc_add"),
    path('send/<int:id_docnum>/', views.doc_result, name="Doc_add_result"),
    path('receive/', views.receivedoc_list, name="Receive_List"),
    path('receive/export/', views.receive_export, name="Receive_Export"),
    path('receive/add/', views.receivedoc_add, name="Receive_add"),
    path('receive/<int:id_rcvdoc>/', views.receivedoc_result, name="Receive_result"),
    path('contract/', views.contract_list, name="Contract_list"),
    path('contract/add/', views.contract_add, name="Contract_add"),
    path('contract/<int:contra_id>/', views.contract_detail, name='Contract_detail'),
    path('contract/<int:contra_id>/update/', views.contract_update, name='Contract_update'),
    path('contract/<int:contra_id>/disable/', views.contract_disable, name='Contract_disable'),
    path('contract/<int:contra_id>/confirm/', views.contract_confirm, name='Contract_confirm'),
]
from django.contrib import admin
from django.urls import path,include
from .views import (view_data_detail,size_data,
base,delete_data,upload_data,predict_csv_single,about,predict_csv_multi,predict_data_manually,view_data,analysis,change_password,login2,account_details,add_files_multi,detection,dashboard,userLogout,reports,upload_credit_data,prediction_button,enter_form_data_manually,add_files_single)
from . import views
#about
urlpatterns = [
    #
    #path('home/', include('Apps.homeApp.urls', namespace='home')),
    #
    
   
    path('',base),
    path('login/',login2,name='login2'),
    path('logout/',userLogout,name='userLogout'),
    path('fraud_detection/',detection,name='detection'),
    path('about/',about,name='about'),
    path('dashboard/',dashboard,name='dashboard'),
    path('reports/',reports,name='reports'),
    path('upload_credit_data/',upload_credit_data,name='upload_credit_data'),
    path('prediction_button/',prediction_button,name='prediction_button'),
    
    #for main adminstrator upload 
    
    path('upload_data/',upload_data,name='upload_data'),
    path('delete_data/<int:id>/',delete_data,name='delete_data'),


    path('enter_form_data_manually/',enter_form_data_manually,name='enter_form_data_manually'),
    path('add_files_single/',add_files_single,name='add_files_single'),
    path('add_files_multi/',add_files_multi,name='add_files_multi'),

    path('predict_data_manually/',predict_data_manually,name='predict_data_manually'),
    path('predict_csv_single/',predict_csv_single,name='predict_csv_single'),
    path('predict_csv_multi/',predict_csv_multi,name='predict_csv_multi'),

    path('account_details/',account_details,name='account_details'),
    path('change_password/',change_password,name='change_password'),
    path('analysis/<str:file_name>/', views.analysis, name='analysis'),
    path('size_data/<str:file_name>/', views.size_data, name='size_data'),
    path('view_data/', views.view_table, name='view_data'),
    path('view_data/<str:file_name>/', views.view_data_detail, name='view_data_detail'),
    
]

#path('about/',about,name='about')

from django.contrib import admin
from django.urls import path
#from my_Apps.views import *
from . import views
from .import chatbotviews
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('',views.homepage,name='homepage'),
    path('home/',views.Home,name='home'),
    path('about/',views.aboutpage,name='aboutpage'),
    path('contact/',views.contactus,name='contactus'),
    path('profile/',views.profile,name='profile'),
    path('chatroom/', chatbotviews.chatroom, name= 'chatroom'),

    path('login/',views.loginpage,name='loginpage'),
    path('logout/',views.Logout,name='logout'),
    path('adminlogout/',views.Logout_admin,name='adminlogout'),
    path('createaccount',views.createaccountpage,name='createaccountpage'),

    path('patienthome/', views.patienthome, name='patienthome'),
    path('doctorhome/', views.doctorhome, name='doctorhome'),
    path('adminhome/', views.adminhome, name='adminhome'),
    
    path('adminaddDoctor/',views.adminaddDoctor,name='adminaddDoctor'),
    path('adminviewDoctor/',views.adminviewDoctor,name='adminviewDoctor'),
    path('adminDeleteDoctor<int:pid><str:email>',views.admin_delete_doctor,name='admin_delete_doctor'),
    path('adminviewAppointment/',views.adminviewAppointment,name='adminviewAppointment'),
    
    path('makeappointments/',views.MakeAppointments,name='makeappointments'),
    path('viewappointments/',views.viewappointments,name='viewappointments'),
    path('viewhealthrecords/',views.viewhealthrecords,name='viewhealthrecords'),
    
    path('PatientDeleteAppointment<int:pid>',views.patient_delete_appointment,name='patient_delete_appointment'),
    path('PatientHome',views.patienthome,name='patienthome'),
    path('get-available-time-slots/', views.get_available_time_slots, name='get_available_time_slots'),

    path('updatepassword/',views.updatepassword,name='updatepassword'),
    #For Forgot Password and Reset Password
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='forgot.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='reset.html'), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='passwordresetcomplete.html'), name="password_reset_complete"),

    

]
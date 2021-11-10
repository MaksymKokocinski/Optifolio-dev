from django.urls import path

from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('homepage/', views.homepage, name="homepage"),
    
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    
    path('', views.adminpage, name="adminpage"),
    path('customer/<str:pk>/', views.customer, name='customer'),
    
    path('userpage/', views.userPage, name='userpage'), 
    path('account/', views.accountSettings, name ='account'),
 


    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="optifolio/password_reset.html")
    ,name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="optifolio/password_reset_sent.html")
    ,name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="optifolio/password_reset_form.html")
    ,name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="optifolio/password_reset_done.html")
    ,name="password_reset_complete"),


    path('summary/', views.summaryPage, name="summary"),

    path('visualisationpage/', views.visualisationPage, name="visualisationpage"),
    path('templatevisualisationpage/', views.templatevisualisationPage, name="templatevisualisationpage"),

    path('infopage/', views.infoPage, name="infopage"),
]
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings

urlpatterns = [
    path('homepage/', views.homepage, name="homepage"),
    
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    
    path('', views.adminpage, name="adminpage"),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('delete_customer/<str:pk>/', views.delete_customer, name='delete_customer'),

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
    path('vispage/<str:pk>/', views.visPage, name='vispage'),
    path('delete_portfolio/<str:pk>/', views.deletePortfolio, name="delete_portfolio"),
    path('portfolio_state/<str:pk>/', views.portfolioState, name="portfolio_state"),
    path('optimize/<str:pk>/', views.portfolioOptimize, name="optimize"),

    path('visualisationpage/', views.visualisationPage, name="visualisationpage"),
    path('add_transaction/<str:pk>/', views.addVisData, name="add_transaction"),
    path('update_transaction/<int:vispk>/', views.updateVisData, name="update_transaction"),
    path('delete_transaction/<int:vispk>/', views.deleteVisData, name="delete_transaction"),

    path('templatevisualisationpage/', views.templatevisualisationPage, name="templatevisualisationpage"),

    path('infopage/', views.infoPage, name="infopage"),
    path('yahoo/', views.yahooPage, name="yahoo")
]
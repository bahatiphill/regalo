from django.urls import path
'''from .views import ( HomePageView,
    ContactUsView,
    gutura,
    paymentcompletion,
    pendingPayment,
    ChurchesList,
    dash,
    stats,
    kubikuza,
    sentmoney,
    contact_us
    )
'''
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name="home"),
    path('contact_us/', views.ContactUsView.as_view(), name="contact_us"),
    path('gutura/<church_slug>/', views.gutura, name='gutura' ),
    path('paymentcompletion/', views.paymentcompletion, name='paymentcompletion'),
    path('pending/', views.pendingPayment.as_view(), name="pendingPayment"),
    path('churches/', views.ChurchesList.as_view(), name='churches_list'),
    path('dash/', views.dash, name="dashboard"),
    path('delete/<church_slug>', views.delete_, name='delete_'),
    path('delete/<church_slug>/confirmed/', views.delete_church ,name='delete_church'),
    path('overview/', views.overview, name="overview"),
    path('overview/withdraw', views.kubikuza, name="withdraw"),
    path('sentPayment/', views.sentmoney.as_view() ,name='sentPayment'),
]

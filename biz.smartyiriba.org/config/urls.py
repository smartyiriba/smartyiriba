from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from apps.core import views
from apps.commerce import views as commerce_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('expertises/<slug:slug>/', views.service_group, name='service_group'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('formations/', views.trainings, name='trainings'),
    path('solutions/', views.solutions, name='solutions'),
    path('realisations/', views.portfolio, name='portfolio'),
    path('a-propos/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('opportunites/', views.opportunities, name='opportunities'),
    path('documents/', views.legal, name='legal'),
    path('devis/', views.quote, name='quote'),
    path('devis/confirmation/', views.quote_success, name='quote_success'),
    path('compte/', views.dashboard, name='dashboard'),
    path('compte/commandes/', commerce_views.orders, name='orders'),
    path('compte/factures/<str:number>/pdf/', commerce_views.invoice_download, name='invoice_download'),
    path('compte/factures/<str:number>/', commerce_views.invoice_detail, name='invoice_detail'),
    path('inscription/', views.register, name='register'),
    path('connexion/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('deconnexion/', auth_views.LogoutView.as_view(), name='logout'),
]
admin.site.site_header = 'Smart YIRIBA'

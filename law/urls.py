from django.urls import path
from . import views

app_name = 'law'

urlpatterns = [
    path('', views.home, name='home'),
    path('hakkimizda/', views.about, name='about'),
    path('hizmetlerimiz/', views.services, name='services'),
    path('iletisim/', views.contact, name='contact'),
    path('blog/', views.blog_list, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('basari-hikayeleri/', views.success_stories, name='success_stories'),
    path('sikca-sorulan-sorular/', views.faq, name='faq'),
    path('yasal-uyarilar/', views.legal_notice, name='legal_notice'),
] 
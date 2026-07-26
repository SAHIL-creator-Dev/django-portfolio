from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('robots.txt', TemplateView.as_view(template_name="core/robots.txt", content_type="text/plain")),
    path('sitemap.xml', TemplateView.as_view(template_name="core/sitemap.xml", content_type="application/xml")),
]

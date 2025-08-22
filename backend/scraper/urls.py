from django.urls import path
from . import views

urlpatterns = [
    path('api/auth/google/', views.google_auth_verify, name='google_auth_verify'),
    path('api/scrape/', views.scrape_url, name='scrape_url'),
    path('api/items/', views.list_items, name='list_items'),
]

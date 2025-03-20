from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('month/', views.show_month, name='show_month'),
    path('week/', views.show_week, name='show_week'),
    path('entry/<int:entry_id>/', views.entry_detail, name='entry_detail'),
    path('track', views.add_entry, name='add_entry'),
    path('edit/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]
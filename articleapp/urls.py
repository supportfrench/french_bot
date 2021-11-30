from django.urls import path
from articleapp import views

urlpatterns = [
    path('', views.home, name="home"),
    path('history/', views.HistoryView.as_view(), name="history"),
]

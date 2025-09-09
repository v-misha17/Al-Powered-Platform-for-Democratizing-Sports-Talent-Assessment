from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_video, name='upload_video'),
    path('results/<int:assessment_id>/', views.assessment_results, name='assessment_results'),
    path('history/', views.assessment_history, name='assessment_history'),
]
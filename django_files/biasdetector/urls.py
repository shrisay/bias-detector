from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('detect', views.detect_view, name="detect_view"),
    path('about', views.about_us, name="about"),
    path('howitworks', views.howitworks, name="howitworks"),
    path('feedback', views.feedback, name="feedback"),
    path('view/feedback', views.view_feedback, name="view_feedback"),

    path('api/analyze/', views.analyze_api, name="analyze")
]

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('upload/', views.FileUploadView.as_view(), name='file-upload'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('documents/', views.UserDocumentsView.as_view(), name='document-list'),
]

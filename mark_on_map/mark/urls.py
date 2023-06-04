from django.urls import path
from . import views

urlpatterns = [
    path('mark/',views.UploadView, name='mark'),
]
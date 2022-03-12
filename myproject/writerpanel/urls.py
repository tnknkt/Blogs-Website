from django.urls import path
from .views import panel,displayForm,insertData

urlpatterns = [
    path('',panel,name="panel"),
    path('displayForm',displayForm,name="displayForm"),
    path('insertData',insertData,name="insertData"),
]

from atexit import register
from django.urls import path
from .views import index,register

urlpatterns=[
    path('member', index,name="member"),
    path('register/add',register,name="addUser"),
]
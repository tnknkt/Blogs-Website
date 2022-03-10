from django.urls import path
from .views import index,blogDetail,searchCategory

urlpatterns = [
    path('', index),
    path('blog/<int:id>',blogDetail,name="blogDetail"),
    path('blog/category/<int:cat_id>',searchCategory,name="searchCategory")
    ]

from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard/',
         RedirectView.as_view(pattern_name='home', permanent=False),
         name='Blog_Dashboard'),
    path('posts/',
         views.Blog_Post_Display,
         name="Blog_Post_Display"),
    path('posts/delete/<int:id>',
         views.Blog_Post_Delete,
         name="Blog_Post_Delete")
]
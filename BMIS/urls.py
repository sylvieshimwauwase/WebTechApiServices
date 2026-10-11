"""
URL configuration for BMIS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('home/', views.home, name='home_alias'),
    path('', views.home, name='home'), # Root URLs

    # Learning Dynamic URLs
    # Integer Dynamic URL
    path('course/<int:course_id>', views.course),
    path('courseName/<str:course_name>', views.courseName),
    path('courseBlog/<slug:course_blog_title>', views.courseBlog),
    path("studentMarks/", views.studentMarks),

    # including app urls in project urls
    path('blog/',include('Blog.urls'))
]

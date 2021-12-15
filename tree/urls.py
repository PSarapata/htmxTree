"""htmxTree URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from tree.views import TreeList, expand, collapse, sort_us


urlpatterns = [
    path('', TreeList.as_view(), name='tree_list'),
    path('expand/<int:tree_id>/', expand, name='tree_expand'),
    path('collapse/<int:tree_id>/', collapse, name='tree_collapse'),
    path('sort_us/', sort_us, name='tree_sort_us'),
]

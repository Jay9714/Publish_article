"""publish_article URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from blog import views
from django.conf import settings  
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='index'),
    path('registration/', views.registration,name='registration'),
    path('loginview/', views.loginview,name='loginview'),
    path('logoutview/', views.logoutview,name='logoutview'),
    path('main_page/', views.main_page,name='main_page'),
    path('article/', views.article,name='article'),
    path('draft/', views.draft,name='draft'),
    path('edit_draft/<int:id>/', views.edit_draft,name='edit_draft'),
    path('delete_draft/<int:id>/', views.delete_draft,name='delete_draft'),
    path('delete_article/<int:id>/', views.delete_article,name='delete_article'),
    path('tag_post/<int:id>/', views.tag_post,name='tag_post'),
    path('tag_delete/<int:id>/<int:tag_id>/', views.tag_delete,name='tag_delete'),



]
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  

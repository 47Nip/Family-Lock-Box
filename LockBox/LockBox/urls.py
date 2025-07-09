"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from myapp import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('nav.html',views.navpage,name='navpage'),
    path('',views.homepage , name='homepage'),
    path('signin.html',views.signuppage,name='signuppage'),
    path('login.html',views.loginpage,name='loginpage'),
    path('upload.html', views.uploadpage, name='upload_file'),
    path('documentview.html',views.documentpage,name='documentpage'),
    path('profile.html',views.profilepage,name='profilepage'),
    path('logout.html', views.logout_view, name='logout'),
    path('membergroup.html',views.groupmember,name='groupmember'),
    path('yourgroups.html',views.yourgroups,name='yourgroups'),
    path('group_document/<str:matched_username>/', views.groupdocument, name='groupdocument'),
    path('document/rename/<int:file_id>/', views.rename_document, name='rename_document'),
    path('document/delete/<int:file_id>/', views.delete_document, name='delete_document'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""rutherford_john_final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),

    path("login/",
         TemplateView.as_view(template_name='calorie_counter/login.html'),
         name="login_urlpattern"
        ),

    path('', include('calorie_counter.urls')),

    path('',
         RedirectView.as_view(
                pattern_name='calorie_counter_member_list_urlpattern',
                permanent=False
         )),

    path('about/',
            TemplateView.as_view(
                template_name='calorie_counter/about.html'),
                name='about_urlpattern'
         ),
]
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
from django.urls import path
from calcapp.views import calculate, login_view
import logging

##3 로거 생성 ###
logger = logging.getLogger(__name__)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),  # 초기 페이지
    path('login/', login_view, name='login'),  # 로그인 페이지
    path('calculate/', calculate, name='calculate'),  # 계산 페이지 (views.py 참조)
]

### 로깅 추가 ###
logger.info('URL configuration loaded successfully.')
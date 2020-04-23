from django.contrib import admin
from django.urls import path, include
from crypto.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("crypto.urls")),

]

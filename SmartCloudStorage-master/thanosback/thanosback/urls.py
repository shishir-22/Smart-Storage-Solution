from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url('form/',include('form.urls')),
    url('admin/',admin.site.urls),
]
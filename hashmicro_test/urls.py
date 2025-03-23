from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403, handler404
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path("module/", include("engine.urls")),
    path('product/', include('product.urls')),
]

def custom_403(request, exception):
    return render(request, "errors/403.html", status=403)

def custom_404(request, exception):
    return render(request, "errors/404.html", status=404)

handler403 = custom_403
handler404 = custom_404

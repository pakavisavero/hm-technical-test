from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403, handler404
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView

from engine.views import login_view, logout_view, dashboard_view

urlpatterns = [
    path("", login_view, name="login"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"), 
    path("dashboard/", dashboard_view, name="dashboard"),
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('accounts/profile/', lambda request: redirect('dashboard'), name='profile_redirect'),  
    path("module/", include("engine.urls")),
    path('product/', include('product.urls')),
]

def custom_403(request, exception):
    return render(request, "errors/403.html", status=403)

def custom_404(request, exception):
    return render(request, "errors/404.html", status=404)

handler403 = custom_403
handler404 = custom_404


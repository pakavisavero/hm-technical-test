from django.shortcuts import render
from .models import Module

class ModuleCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/") or request.path.startswith("/module/"):
            return self.get_response(request)

        path_parts = request.path.strip("/").split("/")

        if path_parts:  
            module_name = path_parts[0]
            module = Module.objects.filter(name=module_name, installed=True).first()
            if not module:
                return render(request, "errors/404.html", status=404)

        return self.get_response(request)

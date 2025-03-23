from django.shortcuts import render
from .models import Module

class ModuleCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path_parts = request.path.strip("/").split("/")
        if not path_parts:
            return self.get_response(request)

        if path_parts[0] in ["accounts", "admin", "dashboard", "static", "media"]:
            return self.get_response(request)

        module_name = path_parts[0]

        try:
            module = Module.objects.get(name=module_name)
            if not module.installed:
                return render(request, "errors/404.html", status=404)
        except Module.DoesNotExist:
            pass

        return self.get_response(request)
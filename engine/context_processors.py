from .models import Module
import re

def module_apps(request):
    modules = Module.objects.all()
    for module in modules:
        module.display_name = re.sub(r"([A-Z])", r" \1", module.name).strip()
    return {'module_apps': modules}
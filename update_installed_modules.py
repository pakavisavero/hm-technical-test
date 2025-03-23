import json
import os
import django

# Set up Django before importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hashmicro_test.settings")
django.setup()

from django.conf import settings
from engine.models import Module

def update_installed_modules():
    """Fetch installed modules from DB and save them to a JSON file."""
    installed_modules = list(Module.objects.filter(installed=True).values_list("name", flat=True))
    modules_file = os.path.join(settings.BASE_DIR, "installed_modules.json")

    with open(modules_file, "w") as f:
        json.dump(installed_modules, f)

    print(f"Updated installed modules: {installed_modules}")

if __name__ == "__main__":
    update_installed_modules()

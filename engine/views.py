from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.urls import clear_url_caches, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from engine.permissions import assign_module_permissions
from engine.decorators import role_required

from .models import Module
import subprocess
import os
import re

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages



def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse("dashboard"))

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")

            return redirect(reverse("dashboard"))

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "auth/login.html")


def logout_view(request):
    """
    Logs out the user and redirects to the login page.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")  # Ensure 'login' is the name of your login URL


@login_required
def dashboard_view(request):
    """
    Display the dashboard page with a welcome message.
    """
    return render(request, "dashboard.html", {"title": "Dashboard"})


@login_required
@role_required(["manager"])
def module_list(request):
    """
    Retrieves all available modules and renders the module management page.
    
    @param request: Django HTTP request object.
    @return: Rendered HTML template with module data.
    """
    modules = Module.objects.all()
    return render(request, "engine/module_list.html", {"modules": modules})


@login_required
@role_required(["manager"])
def create_module(request):
    """
    * Handles module creation.
    * * 1. Validates input and checks for duplicate names.
    * 2. Creates a new module record in the database.
    * 3. Generates the necessary Django app files and directories.
    * 4. Updates project URLs to include the new module.
    *
    * @param request: Django HTTP request object.
    * @return: Redirects to module list page with success/error messages.
    """
    if request.method == "POST":
        module_name = request.POST.get("module_name", "").lower().strip()

        if re.search(r'[^a-zA-Z0-9_]', module_name):
             messages.error(request, "Module name must contain only alphanumeric characters and underscores.")
             return redirect("module_list")

        module_name = re.sub(r'[^a-zA-Z0-9_]', '', module_name).lower()

        if not module_name:
            messages.error(request, "Module name is required.")
            return redirect("module_list")

        if Module.objects.filter(name=module_name).exists():
            messages.error(request, f"Module '{module_name}' already exists.")
            return redirect("module_list")

        # Create module record with installed=False
        module = Module.objects.create(name=module_name, installed=False)

        project_path = settings.BASE_DIR
        app_path = os.path.join(project_path, module_name)

        if os.path.exists(app_path):
            messages.error(request, f"Module '{module_name}' already exists in the file system.")
            return redirect("module_list")

        try:
            subprocess.run(["python", "manage.py", "startapp", module_name], check=True)
        except subprocess.CalledProcessError:
            messages.error(request, f"Failed to create Django app '{module_name}'.")
            return redirect("module_list")

        engine_templates_path = os.path.join(project_path, "engine", "templates", module_name)
        os.makedirs(engine_templates_path, exist_ok=True)

        with open(os.path.join(app_path, "urls.py"), "w") as f:
            f.write(f"""
from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='{module_name}_list'),
]
            """.strip())

        with open(os.path.join(app_path, "views.py"), "w") as f:
            f.write(f"""
from django.shortcuts import render

def index(request):
    return render(request, '{module_name}/index.html', {{'module_name': '{module_name}'}})
            """.strip())

        with open(os.path.join(engine_templates_path, "index.html"), "w") as f:
            f.write(f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{{ module_name }}} Module</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
      body {{
        background: linear-gradient(135deg, #e0f7fa, #b2ebf2);
      }}
      .module-card {{
        background: white;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      }}
      .home-button {{
        background: linear-gradient(to right, #6366f1, #8b5cf6);
      }}
    </style>
  </head>
  <body class="flex items-center justify-center h-screen">
    <div class="module-card text-center p-8 rounded-2xl w-96">
      <h1 class="text-3xl font-bold text-gray-800 mb-4 tracking-tight">{{{ module_name }}} Module</h1>
      <p class="text-gray-600 mb-6">The module is ready, but requires further configuration.</p>
      <a href="/dashboard" class="home-button mt-6 inline-block px-6 py-3 text-white text-lg rounded-xl hover:bg-indigo-600 transition-colors font-semibold">
        Go Home
      </a>
    </div>
  </body>
</html>
            """.strip())

        project_urls_path = os.path.join(project_path, "hashmicro_test", "urls.py")
        try:
            with open(project_urls_path, "r+") as f:
                urls_content = f.read()
                new_include = f"    path('{module_name}/', include('{module_name}.urls')),\n"
                if new_include not in urls_content:
                    end_of_urlpatterns = urls_content.find("]")
                    if end_of_urlpatterns != -1:
                        urls_content = urls_content[:end_of_urlpatterns] + new_include + urls_content[end_of_urlpatterns:]
                        f.seek(0)
                        f.write(urls_content)
                    else:
                        messages.error(request, "Failed to find urlpatterns in project URLs.")
                        return redirect("module_list")
        except Exception as e:
            messages.error(request, f"Failed to update project URLs: {str(e)}")
            return redirect("module_list")

        messages.success(request, f"Module '{module_name}' created successfully.")
        return redirect("module_list")

    messages.error(request, "Invalid request method.")
    return redirect("module_list")


def run_migrations_for_module(app_name, is_install=False):
    """
    Runs database migrations only for the specified app.

    @param app_name: The name of the Django app related to the module.
    @param is_install: If True, runs migrations for all apps.
    @return: Tuple (success: bool, message: str)
    """
    project_path = settings.BASE_DIR
    try:
        if is_install:
            subprocess.run(["python", "manage.py", "makemigrations"], cwd=project_path, check=True)
            subprocess.run(["python", "manage.py", "migrate"], cwd=project_path, check=True)
            return True, "Migrations applied for all apps."
        else:
            subprocess.run(["python", "manage.py", "makemigrations", app_name], cwd=project_path, check=True)
            subprocess.run(["python", "manage.py", "migrate", app_name], cwd=project_path, check=True)
            return True, f"Migrations applied for '{app_name}'."
    except subprocess.CalledProcessError as e:
        return False, f"Migration error: {str(e)}"


def rollback_migrations_for_module(app_name):
    """
    Rolls back all migrations for a specific app by migrating it to 'zero'.
    
    @param app_name: The name of the Django app related to the module.
    @return: (bool, message) Tuple indicating success or failure.
    """
    project_path = settings.BASE_DIR
    try:
        subprocess.run(["python", "manage.py", "migrate", app_name, "zero"], cwd=project_path, check=True)
        return True, f"Migrations rolled back for '{app_name}'."
    except subprocess.CalledProcessError as e:
        return False, f"Error rolling back migrations for '{app_name}': {str(e)}"


@login_required
@role_required(["manager"])
def install_module(request, module_name):
    """
    Installs a module, runs migrations, and assigns necessary permissions.
    """
    module = get_object_or_404(Module, name=module_name)

    if module.installed:
        messages.warning(request, f"Module '{module_name}' is already installed.")
        return redirect("module_list")

    module.installed = True
    module.save()
    
    # Update installed modules file
    os.system("python update_installed_modules.py")

    app_name = module_name.lower()
    success, message = run_migrations_for_module(app_name, is_install=True)
    
    if success:
        messages.success(request, f"Module '{module_name}' installed successfully. {message}")
        assign_module_permissions(app_name)
    else:
        messages.error(request, message)

    return redirect("module_list")


@login_required
@role_required(["manager"])
def upgrade_module(request, module_name):
    """
    * Upgrades a module by updating its version.
    * 
    * 1. Retrieves the module.
    * 2. Updates the version to the user-specified value.
    * 3. Saves the updated version to the database.
    *
    * @param request: Django HTTP request object.
    * @param module_name: Name of the module to upgrade.
    * @return: Redirects to module list page with success/error messages.
    """

    module = get_object_or_404(Module, name=module_name)

    if request.method == "POST":
        desired_version = request.POST.get("version", "").strip()   
    else:
        desired_version = request.GET.get("version", "").strip()

    if not desired_version:
        messages.error(request, "Please provide a valid version number.")
        return redirect("module_list")  
    
    # Ensure the version contains only numbers and dots (e.g., "1.0.3")
    if not re.match(r"^\d+(\.\d+)*$", desired_version):
        messages.error(request, "Invalid version format. Use numbers and dots only.")
        return redirect("module_list")

    module.version = desired_version
    module.save()
    
    # Run migrations for the module
    app_name = module_name.lower()
    success, message = run_migrations_for_module(app_name)
    if not success:
        messages.error(request, message)
        return redirect("module_list")
    
    messages.success(request, f"Module '{module_name}' upgraded to version {desired_version}.")
    return redirect("module_list")


@login_required
@role_required(["manager"])
def uninstall_module(request, module_name):
    """
    * Uninstalls a module and rolls back its database migrations.
    *
    * 1. Retrieves the module.
    * 2. Marks the module as uninstalled in the database.
    * 3. Rolls back migrations for the specific module.
    * 4. Clears URL caches to refresh the routing system.
    * 5. Returns a success/error message.
    *
    * @param request: Django HTTP request object.
    * @param module_name: Name of the module to uninstall.
    * @return: Redirects to module list page with success/error messages.
    """
    module = Module.objects.filter(name=module_name).first()
    
    if not module:
        messages.error(request, f"Module '{module_name}' not found.")
        return redirect("module_list")

    success, msg = rollback_migrations_for_module(module_name)
    if not success:
        messages.error(request, msg)
        return redirect("module_list")

    module.installed = False
    module.save()
    
    # Update installed modules file
    os.system("python update_installed_modules.py")
    
    clear_url_caches()

    messages.success(request, f"Module '{module_name}' uninstalled and migrations rolled back successfully.")
    return redirect("module_list")
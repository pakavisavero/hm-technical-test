from django.urls import path
from .views import module_list, create_module, install_module, uninstall_module, upgrade_module

urlpatterns = [
    path("", module_list, name="module_list"),
    path("create/", create_module, name="create_module"),
    path("install/<str:module_name>/", install_module, name="install_module"),
    path("uninstall/<str:module_name>/", uninstall_module, name="uninstall_module"),
    path("upgrade/<str:module_name>/", upgrade_module, name="upgrade_module"),
]

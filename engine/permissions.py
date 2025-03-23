from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

def assign_module_permissions(app_name):
    """
    Assigns permissions dynamically for all models in the specified module.

    - Manager: Can Create, Read, Update, Delete (CRUD)
    - User: Can Create, Read, Update (CRU)
    - Public: Can only Read (R)
    """
    role_permissions = {
        "manager": ["add", "change", "delete", "view"],
        "user": ["add", "change", "view"],
        "public": ["view"],
    }

    try:
        models = apps.get_app_config(app_name).get_models()

        for model in models:
            content_type = ContentType.objects.get_for_model(model)

            for role, actions in role_permissions.items():
                group, _ = Group.objects.get_or_create(name=role)

                for action in actions:
                    permission_codename = f"{action}_{model._meta.model_name}"
                    
                    try:
                        permission = Permission.objects.get(
                            codename=permission_codename,
                            content_type=content_type
                        )
                        group.permissions.add(permission)
                    except Permission.DoesNotExist:
                        print(f"Permission '{permission_codename}' does not exist.")

    except Exception as e:
        print(f"Error assigning permissions for {app_name}: {e}")

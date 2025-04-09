from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from engine.models import Module

def create_roles():
    """Creates the 'superadmin', 'manager', 'user', and 'public' roles and sets permissions."""
    superadmin_group, _ = Group.objects.get_or_create(name="superadmin")
    manager_group, _ = Group.objects.get_or_create(name="manager")
    user_group, _ = Group.objects.get_or_create(name="user")
    Group.objects.get_or_create(name="public")

    module_content_type = ContentType.objects.get_for_model(Module)

    # Manager permissions (CRUD)
    manager_perms = [
        Permission.objects.get_or_create(codename=f"add_{Module._meta.model_name}", content_type=module_content_type)[0],
        Permission.objects.get_or_create(codename=f"change_{Module._meta.model_name}", content_type=module_content_type)[0],
        Permission.objects.get_or_create(codename=f"delete_{Module._meta.model_name}", content_type=module_content_type)[0],
        Permission.objects.get_or_create(codename=f"view_{Module._meta.model_name}", content_type=module_content_type)[0],
    ]
    manager_group.permissions.set(manager_perms)

    # User permissions (CRU)
    user_perms = [
        Permission.objects.get_or_create(codename=f"add_{Module._meta.model_name}", content_type=module_content_type)[0],
        Permission.objects.get_or_create(codename=f"change_{Module._meta.model_name}", content_type=module_content_type)[0],
        Permission.objects.get_or_create(codename=f"view_{Module._meta.model_name}", content_type=module_content_type)[0],
    ]
    user_group.permissions.set(user_perms)

    # Superadmin gets all permissions
    all_perms = Permission.objects.all()
    superadmin_group.permissions.set(all_perms)

def create_users():
    """Creates users and assigns them to their respective roles."""
    superadmin_group = Group.objects.get(name="superadmin")
    manager_group = Group.objects.get(name="manager")
    user_group = Group.objects.get(name="user")

    # Superadmin user
    superadmin_user, created = User.objects.get_or_create(username="hashmicro")
    if created:
        superadmin_user.set_password("test@2025")
        superadmin_user.is_superuser = True
        superadmin_user.is_staff = True
        superadmin_user.save()
        superadmin_user.groups.add(superadmin_group)
        superadmin_user.user_permissions.set(Permission.objects.all())

    # Manager user
    manager_user, created = User.objects.get_or_create(username="manager")
    if created:
        manager_user.set_password("managerpassword")
        manager_user.save()
        manager_user.groups.add(manager_group)

    # Basic user
    user_user, created = User.objects.get_or_create(username="user")
    if created:
        user_user.set_password("userpassword")
        user_user.save()
        user_user.groups.add(user_group)

def create_initial_module():
    """Creates the 'product' module if it doesn't exist."""
    Module.objects.get_or_create(
        name="product",
        defaults={"installed": False, "version": "1.0.0"}
    )

def create_initial_data():
    """Combines the role and user creation functions for easy execution."""
    create_roles()
    create_users()
    create_initial_module()

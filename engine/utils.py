from django.contrib.auth.models import Group, User
from engine.models import Module

def create_roles():
    """Creates the 'manager', 'user', and 'public' roles if they don't exist."""
    roles = ["manager", "user", "public"]
    for role in roles:
        Group.objects.get_or_create(name=role)

def create_users():
    """Creates 'manager' and 'user' accounts and assigns them to their respective roles."""
    manager_group, created = Group.objects.get_or_create(name="manager")
    user_group, created = Group.objects.get_or_create(name="user")

    manager_user, created = User.objects.get_or_create(username="manager")
    if created:
        manager_user.set_password("managerpassword")
        manager_user.save()
        manager_user.groups.add(manager_group)

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

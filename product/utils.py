from django.contrib.auth.models import Group

def create_roles():
    roles = ["manager", "user", "public"]
    for role in roles:
        Group.objects.get_or_create(name=role)

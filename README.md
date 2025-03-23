```sh
from engine.models import Module

Module.objects.create(name="module_example", installed=False, version="1.0.0")
Module.objects.create(name="module_reports", installed=False, version="1.0.0")
Module.objects.create(name="module_dashboard", installed=False, version="1.0.0")

```

```sh
python manage.py shell
>>> from product.utils import create_roles
>>> create_roles()

```

```sh
python manage.py createsuperuser
```
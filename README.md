## Setup and Initialization Guide

This guide outlines the steps to set up and initialize the application.

### ⚙️ Environment Configuration

* **Create `.env` file:**
    * Duplicate `.env.example` to create a `.env` file.
    * Populate the `.env` file with your database configuration:

        ```sh
        DB_ENGINE=<your_database_engine>  # e.g., django.db.backends.sqlite3, django.db.backends.postgresql
        DB_NAME=<your_database_name>      # e.g., db.sqlite3, your_database_name
        ```

    * Replace `<your_database_engine>` and `<your_database_name>` with your actual database settings.

### 💾 Database Migrations

* **Create Migrations:**
    * Generate database migration files based on your models:

        ```sh
        python manage.py makemigrations
        ```

* **Apply Migrations:**
    * Apply the migrations to create the database schema:

        ```sh
        python manage.py migrate
        ```

### 👤 Superuser Creation

* **Create Superuser:**
    * Create an administrator account:

        ```sh
        python manage.py createsuperuser
        ```

    * Follow the prompts to set the username, email, and password.

### 🚀 Initial Data Population

* **Run Initial Data Script:**
    * Execute the script to create initial roles, users, and modules:

        ```sh
        python manage.py create_initial_data
        ```

    * This command calls the `create_initial_data` function, which performs the following database initialization:

        * **Creates Roles (Groups):**
            * The script ensures that the `manager`, `user`, and `public` roles (Django `Group` objects) exist in the database.
            * It uses `Group.objects.get_or_create()` to either retrieve existing roles or create them if they don't exist.
            * This is done using the `create_roles()` function.

        * **Creates Users and Assigns Roles:**
            * It creates two user accounts: `manager` and `user`.
            * For each user, it sets a default password (`managerpassword` and `userpassword` respectively).
            * It then assigns the `manager` user to the `manager` group and the `user` user to the `user` group.
            * This is done using the `create_users()` function.

        * **Creates Initial Module Entry:**
            * It creates an initial entry for the `product` module in the `Module` table.
            * The module is created with `installed=False` and `version="1.0.0"`.
            * This sets up the initial module state for the application.
            * This is done using the `create_initial_module()` function.

        ```python
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
        ```

### 🚀 Run the Development Server

* **Start the Server:**
    * Start the Django development server:

        ```sh
        python manage.py runserver
        ```

    * Access the application in your web browser at `http://127.0.0.1:8000/`.

### 🔑 Default User Credentials

* **Default User Accounts:**
    * The `create_initial_data` script creates two default user accounts:

        * **Manager Account:**
            * Username: `manager`
            * Password: `managerpassword`

        * **User Account:**
            * Username: `user`
            * Password: `userpassword`

    * Use these credentials to log in and test the application's functionality.

### 🧩 Using the Module Management System

After completing the setup and initialization, you can use the module management system to create, install, upgrade, and uninstall modules.

**1. ➕ Creating a Module**

* **Run the module creation command:**
    * Execute the following command to create a new module:

        ```sh
        python manage.py create_module <module_name>
        ```

    * Replace `<module_name>` with the desired name for your module (e.g., `inventory`, `sales`).

* **Command Execution Steps:**
    * The `create_module` command performs the following actions:
        * 📁 **Creates App Folder:** Generates a new Django app folder named `<module_name>` in your project's root directory.
        * 🏗️ **Creates Basic App Structure:** Populates the app folder with essential files like `models.py`, `views.py`, `urls.py`, and `__init__.py`.
        * 🔌 **Registers App in `INSTALLED_APPS`:** Adds the new module to the `INSTALLED_APPS` list in your `settings.py` file, enabling Django to recognize the app.
        * 📄 **Creates Initial Migration:** Runs `python manage.py makemigrations <module_name>` to create initial migration files based on the models defined in `models.py` (if any).
        * 🔗 **Creates Basic URLs and Views:** Creates a basic url and view structure in the `urls.py` and `views.py`.
        * 🚀 **Runs Migration:** Runs `python manage.py migrate <module_name>` to apply the migration to create the database schema.

**2. ✅ Installing a Module**

* **Install the module:**
    * Use the following command to install a module:

        ```sh
        python manage.py install_module <module_name>
        ```

    * Replace `<module_name>` with the name of the module you want to install.

* **Command Execution Steps:**
    * The `install_module` command performs the following actions:
        * ✅ **Sets Module as Installed:** Updates the `installed` field in the `Module` table to `True` for the specified module.
        * 🚀 **Activates the Page/Functionality:** The module becomes accessible within your application, and its associated URLs and views become active.

**3. ⬆️ Upgrading a Module**

* **Upgrade the module:**
    * Use the following command to upgrade a module:

        ```sh
        python manage.py upgrade_module <module_name>
        ```

    * Replace `<module_name>` with the name of the module you want to upgrade.

* **Command Execution Steps:**
    * The `upgrade_module` command performs the following actions:
        * 🔄 **Runs Migrations:** Executes `python manage.py makemigrations <module_name>` followed by `python manage.py migrate <module_name>` to apply any new database schema changes related to the module.
        * 📈 **Updates Module Version:** Updates the `version` field in the `Module` table to reflect the latest version of the module (if applicable).

**4. 🗑️ Uninstalling a Module**

* **Uninstall the module:**
    * Use the following command to uninstall a module:

        ```sh
        python manage.py uninstall_module <module_name>
        ```

    * Replace `<module_name>` with the name of the module you want to uninstall.

* **Command Execution Steps:**
    * The `uninstall_module` command performs the following actions:
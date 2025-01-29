import os
import importlib
import structlog
from registry.manager_registry import ModelManagerRegistry
from config.config import settings

# Initialize structured logging
log = structlog.get_logger()

############################################
# Section: Register all apps and models
############################################

def register_apps(app):
    """
    Automatically detect and register apps in the project.
    For each app found in the directory, it imports the routes module 
    and includes the app's router in the main application.

    Args:
        app: The FastAPI app instance to which the routes should be added.
    """
    apps_dir = os.path.dirname(__file__)
    for app_name in os.listdir(apps_dir):
        app_dir = os.path.join(apps_dir, app_name)
        # Check if it's a directory and doesn't start with '__'
        if os.path.isdir(app_dir) and not app_name.startswith("__"):
            try:
                # Dynamically import the routes module of each app
                module = importlib.import_module(f"apps.{app_name}.routes")
                if hasattr(module, "router"):
                    # Include the router for each app with the API version prefix
                    app.include_router(module.router, prefix=settings.API_V1_PREFIX)
                    log.info("Registered app router", app_name=app_name)
            except ImportError as e:
                log.error("Error importing routes for app", app_name=app_name, error=str(e))

############################################
# Section: Register all model managers
############################################
def register_managers():
    """
    Automatically detect and register model managers for each app.
    For each app found, it imports the manager module and registers the 
    ModelManager in the registry.

    This function ensures that all apps' model managers are registered 
    to manage the respective models appropriately.
    """
    apps_dir = os.path.dirname(__file__)
    for app_name in os.listdir(apps_dir):
        app_dir = os.path.join(apps_dir, app_name)
        # Check if it's a directory and doesn't start with '__'
        if os.path.isdir(app_dir) and not app_name.startswith("__"):
            try:
                # Dynamically import the model manager module for each app
                module = importlib.import_module(f"apps.{app_name}.manager")
                if hasattr(module, "ModelManager"):
                    # Register the ModelManager in the ModelManagerRegistry
                    ModelManagerRegistry.register_manager(app_name, module.ModelManager())
                    log.info("Registered model manager", app_name=app_name)
            except ImportError as e:
                log.error("Error importing manager for app", app_name=app_name, error=str(e))


############################################
# Section: Import all models from each app
############################################

def register_models():
    """
    Automatically detect and import models from all apps.
    For each app found, it attempts to import models from the models directory, 
    including any subfolders and files.

    If any error occurs during the import, it logs an error message.
    """
    apps_dir = os.path.dirname(__file__)
    for app_name in os.listdir(apps_dir):
        app_dir = os.path.join(apps_dir, app_name)
        # Check if it's a directory and doesn't start with '__'
        if os.path.isdir(app_dir) and not app_name.startswith("__"):
            models_module = f"apps.{app_name}.models"
            try:
                # Dynamically import the models module for each app
                importlib.import_module(models_module)
                log.info("Imported models", app_name=app_name)
            except ImportError as e:
                log.error("Error importing models", app_name=app_name, error=str(e))

############################################
# Section: Register all Celery tasks
############################################

def register_celery_tasks():
    """
    Automatically detect and import Celery tasks from all apps.
    For each app found, it attempts to import the tasks.py file.

    If any error occurs during the import, it logs an error message.
    """
    apps_dir = os.path.dirname(__file__)
    for app_name in os.listdir(apps_dir):
        app_dir = os.path.join(apps_dir, app_name)
        # Check if it's a directory and doesn't start with '__'
        if os.path.isdir(app_dir) and not app_name.startswith("__"):
            tasks_module = f"apps.{app_name}.tasks"
            try:
                # Dynamically import the tasks module for each app
                importlib.import_module(tasks_module)
                log.info("Imported Celery tasks", app_name=app_name)
            except ImportError as e:
                log.error("Error importing Celery tasks", app_name=app_name, error=str(e))
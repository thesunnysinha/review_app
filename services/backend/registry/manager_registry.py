class ModelManagerRegistry:
    _managers = {}

    @classmethod
    def register_manager(cls, app_name: str, manager):
        """Register a model manager for an app."""
        cls._managers[app_name] = manager

    @classmethod
    def get_manager(cls, app_name: str):
        """Get a model manager for an app."""
        if app_name not in cls._managers:
            raise ValueError(f"No manager registered for app: {app_name}")
        return cls._managers[app_name]
    
db_manager = ModelManagerRegistry()
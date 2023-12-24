from django.apps import AppConfig


class RessourcesConfig(AppConfig):
    # Sets the default primary key type for models in this app
    default_auto_field = 'django.db.models.BigAutoField'
    # Specifies the name of the app
    name = 'projects'

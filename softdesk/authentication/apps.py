from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
    # Configures the authentication app's settings.
    default_auto_field = 'django.db.models.BigAutoField'  # Sets the default primary key type
    # Specifies the name of the authentication app
    name = 'authentication'

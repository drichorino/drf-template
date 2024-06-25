import os

environment = os.getenv("DJANGO_ENV", "uat")  # Default to UAT if not specified

if environment == "prod":
    from .prod import *
else:
    from .uat import *
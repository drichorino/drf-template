from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import User, UserLog
from .middleware import get_current_request
from .views.auth import user_logged_out


@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
    request = get_current_request()
    description = ""
    if created:
        action = "create"
        description = f"User {instance.username} created"
    else:
        # Check if the save is happening during the login process
        if request and request.path == "/v1/api/auth/":            
            return
        action = "update"
        description = f"User {instance.username} updated"
        if request:
            description += f" by {request.user.username}"

    description += "."

    UserLog.objects.create(user=instance, action=action, description=description)


@receiver(post_delete, sender=User)
def log_user_delete(sender, instance, **kwargs):
    request = get_current_request()
    description = ""
    description = f"User {instance.username} deleted"
    if request:
        description += f" by {request.user.username}"

    description += "."
    UserLog.objects.create(user=instance, action="delete", description=description)


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserLog.objects.create(
        user=user, action="login", description=f"User {user.username} logged in."
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    UserLog.objects.create(
        user=user, action="logout", description=f"User {user.username} logged out."
    )

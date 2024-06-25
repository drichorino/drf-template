from django.db import models

class BlacklistedAccessToken(models.Model):
    token = models.TextField()
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "blacklisted_access_tokens"
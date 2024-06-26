# Generated by Django 5.0.6 on 2024-06-21 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_alter_userlog_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlacklistedAccessToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("token", models.CharField(max_length=255, unique=True)),
                ("blacklisted_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "blacklisted_access_tokens",
            },
        ),
    ]

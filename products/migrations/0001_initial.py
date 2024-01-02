# Generated by Django 4.1.13 on 2024-01-01 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(default="", max_length=200)),
                ("description", models.TextField(default="", max_length=1000)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
                ),
                ("brand", models.CharField(default="", max_length=200)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("Electronics", "Electronics"),
                            ("Clothing", "Clothing"),
                            ("Books", "Books"),
                            ("Sports", "Sports"),
                            ("Home", "Home"),
                            ("Other", "Other"),
                        ],
                        default="Other",
                        max_length=40,
                    ),
                ),
                (
                    "ratings",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
                ),
                ("stock", models.IntegerField(default=0)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
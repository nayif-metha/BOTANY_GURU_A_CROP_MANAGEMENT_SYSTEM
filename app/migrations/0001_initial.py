# Generated by Django 5.1.4 on 2025-01-03 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="login_db",
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
                ("password", models.CharField(max_length=50)),
                ("userid", models.CharField(max_length=50)),
                ("status", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="registration_db",
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
                ("idno", models.IntegerField()),
                ("name", models.CharField(max_length=50)),
                ("address", models.CharField(max_length=50)),
                ("city", models.CharField(max_length=50)),
                ("userid", models.CharField(max_length=50)),
                ("profile", models.FileField(upload_to="")),
            ],
        ),
    ]

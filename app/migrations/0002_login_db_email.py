# Generated by Django 5.1.4 on 2025-01-06 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="login_db",
            name="email",
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]

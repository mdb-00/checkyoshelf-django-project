# Generated by Django 5.0.3 on 2024-05-24 03:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0019_remove_bookshelf_profile_bookshelf_profile"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bookshelf",
            name="profile",
        ),
        migrations.AddField(
            model_name="bookshelf",
            name="profile",
            field=models.ManyToManyField(
                blank=True, related_name="profile", to="app.profile"
            ),
        ),
    ]

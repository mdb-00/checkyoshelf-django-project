# Generated by Django 5.0.3 on 2024-05-14 23:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0014_book_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="profile",
            field=models.ManyToManyField(blank=True, to="app.profile"),
        ),
    ]
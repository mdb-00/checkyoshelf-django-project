# Generated by Django 5.0.3 on 2024-05-24 00:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0017_alter_review_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookshelf",
            name="profile",
            field=models.ManyToManyField(blank=True, to="app.profile"),
        ),
    ]

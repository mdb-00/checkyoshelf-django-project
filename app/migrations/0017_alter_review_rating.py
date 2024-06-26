# Generated by Django 5.0.3 on 2024-05-17 00:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0016_remove_book_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="rating",
            field=models.FloatField(
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(5.0),
                ],
            ),
        ),
    ]

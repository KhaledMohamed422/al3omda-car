# Generated by Django 5.2.3 on 2025-07-10 07:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Governorate",
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
                (
                    "governorate_name_ar",
                    models.CharField(
                        blank=True,
                        help_text="دخل اسم المحافظة باللغة العربية",
                        max_length=50,
                        null=True,
                        unique=True,
                        verbose_name="اسم المحافظة",
                    ),
                ),
                (
                    "governorate_name_en",
                    models.CharField(
                        blank=True,
                        help_text="دخل اسم المحافظة باللغة الإنجليزية",
                        max_length=50,
                        null=True,
                        unique=True,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Governorates",
                "ordering": ["governorate_name_ar"],
            },
        ),
        migrations.CreateModel(
            name="City",
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
                (
                    "city_name_ar",
                    models.CharField(
                        blank=True,
                        help_text="دخل اسم المدينة باللغة العربية",
                        max_length=50,
                        null=True,
                        unique=True,
                        verbose_name="اسم المدينة",
                    ),
                ),
                (
                    "city_name_en",
                    models.CharField(
                        blank=True,
                        help_text="دخل اسم المدينة باللغة الإنجليزية",
                        max_length=50,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "governorate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cities",
                        to="locations.governorate",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Cities",
            },
        ),
    ]

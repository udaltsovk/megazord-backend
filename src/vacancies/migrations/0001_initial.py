# Generated by Django 5.1 on 2024-08-20 23:03

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("teams", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Vacancy",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="teams.team"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Keyword",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("text", models.CharField(max_length=100)),
                (
                    "vacancy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vacancies.vacancy",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Apply",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="teams.team"
                    ),
                ),
                (
                    "who_responsed",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "vac",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vacancies.vacancy",
                    ),
                ),
            ],
        ),
    ]

# Generated by Django 4.1 on 2023-07-25 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("calorie_counter", "0006_calorie_counter_create_group_permissions"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="member",
            options={"ordering": ["last_name", "first_name", "disambiguator"]},
        ),
    ]

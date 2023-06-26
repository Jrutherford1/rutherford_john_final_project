# Generated by Django 4.1 on 2023-06-26 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CalorieGoal",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("target_calories", models.IntegerField()),
                ("begin_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="DailyMacroGoal",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("protein_goal", models.IntegerField()),
                ("carbohydrate_goal", models.IntegerField()),
                ("fat_goal", models.IntegerField()),
                ("date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Exercise",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("exercise_type", models.CharField(max_length=50)),
                (
                    "exercise_category",
                    models.CharField(
                        choices=[("Aerobic", "Aerobic"), ("Anaerobic", "Anaerobic")],
                        default="Aerobic",
                        max_length=10,
                    ),
                ),
                ("calories_burned_per_minute", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="ExerciseLog",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateField()),
                (
                    "duration",
                    models.DecimalField(
                        decimal_places=2, help_text="Duration in minutes", max_digits=5
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Food",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50)),
                ("calories_per_serving", models.IntegerField()),
                ("protein_grams", models.IntegerField()),
                ("carbohydrates_grams", models.IntegerField()),
                ("fat_grams", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="MealFood",
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
                    "quantity",
                    models.DecimalField(
                        decimal_places=2, help_text="Serving size:", max_digits=5
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MealLog",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateField()),
                ("time", models.TimeField()),
                (
                    "meal_type",
                    models.CharField(
                        choices=[
                            ("Breakfast", "Breakfast"),
                            ("Lunch", "Lunch"),
                            ("Dinner", "Dinner"),
                            ("Snack", "Snack"),
                        ],
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Member",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("e_mail", models.EmailField(max_length=254, unique=True)),
                ("height", models.IntegerField(help_text="Height in inches")),
                ("weight", models.IntegerField(help_text="Weight in pounds")),
                ("age", models.IntegerField(help_text="Age in years")),
                (
                    "sex",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")],
                        help_text="Male = M, Female = F",
                        max_length=1,
                    ),
                ),
                ("date_joined", models.DateField()),
            ],
        ),
        migrations.AddConstraint(
            model_name="member",
            constraint=models.UniqueConstraint(
                fields=("first_name", "last_name", "e_mail"), name="unique_member"
            ),
        ),
        migrations.AddField(
            model_name="meallog",
            name="member",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="meal_logs",
                to="calorie_counter.member",
            ),
        ),
        migrations.AddField(
            model_name="mealfood",
            name="food",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="meal_foods",
                to="calorie_counter.food",
            ),
        ),
        migrations.AddField(
            model_name="mealfood",
            name="meal_log",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="meal_foods",
                to="calorie_counter.meallog",
            ),
        ),
        migrations.AddConstraint(
            model_name="food",
            constraint=models.UniqueConstraint(fields=("name",), name="unique_food"),
        ),
        migrations.AddField(
            model_name="exerciselog",
            name="exercise",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="exercise_logs",
                to="calorie_counter.exercise",
            ),
        ),
        migrations.AddField(
            model_name="exerciselog",
            name="member",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exercise_logs",
                to="calorie_counter.member",
            ),
        ),
        migrations.AddConstraint(
            model_name="exercise",
            constraint=models.UniqueConstraint(
                fields=("exercise_type",), name="unique_exercise"
            ),
        ),
        migrations.AddField(
            model_name="dailymacrogoal",
            name="member",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="daily_macro_goals",
                to="calorie_counter.member",
            ),
        ),
        migrations.AddField(
            model_name="caloriegoal",
            name="member",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="calorie_goals",
                to="calorie_counter.member",
            ),
        ),
    ]

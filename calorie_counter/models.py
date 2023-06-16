from django.db import models
from django.db.models import UniqueConstraint


class MealLog(models.Model):
    meal_log_id = models.AutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()
    member = models.ForeignKey('Member', related_name='meal_logs', on_delete=models.PROTECT)
    meal = models.ForeignKey('Meal', related_name='meal_logs', on_delete=models.PROTECT)

    def __str__(self):
        return '%s' % self.meal_log_id



class Meal(models.Model):
    meal_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    food = models.ForeignKey('Food', related_name='meals', on_delete=models.PROTECT)

    def __str__(self):
        return '%s' % self.meal_id


class ExerciseLog(models.Model):
    exercise_log_id = models.AutoField(primary_key=True)
    date = models.DateField()
    duration = models.TimeField()
    member = models.ForeignKey('Member', related_name='exercise_logs', on_delete=models.PROTECT)
    exercise = models.ForeignKey('Exercise', related_name='exercise_logs', on_delete=models.PROTECT)

    def __str__(self):
        return '%s' % self.exercise_log_id

class Exercise(models.Model):
    exercise_id = models.AutoField(primary_key=True)
    exercise_type = models.CharField(max_length=50)
    calories_burned_per_minute = models.IntegerField()

    def __str__(self):
        return '%s' % self.exercise_id


class DailyMacroGoal(models.Model):
    daily_macro_id = models.AutoField(primary_key=True)
    protein_goal= models.IntegerField()
    carbohydrate_goal = models.IntegerField()
    fat_goal = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return '%s' % self.daily_macro_id


class CalorieGoal(models.Model):
    calorie_goal_id = models.AutoField(primary_key=True)
    target_calories = models.IntegerField()
    begin_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return '%s' % self.calorie_goal_id


class Food(models.Model):
    food_id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=50)
    calories_per_serving = models.IntegerField()
    protein_grams = models.IntegerField()
    carbohydrates_grams = models.IntegerField()
    fat_grams = models.IntegerField()

    def __str__(self):
        return '%s' % self.food_id


class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    e_mail = models.CharField(max_length=50)
    height = models.IntegerField()
    weight = models.IntegerField()
    age = models.IntegerField()
    sex = models.CharField(max_length=1)
    calorie_goal = models.ForeignKey(CalorieGoal, related_name='members', on_delete=models.PROTECT)
    daily_macro_goal = models.ForeignKey(DailyMacroGoal, related_name='members', on_delete=models.PROTECT)
    date_joined = models.DateField()
    meal_log = models.ForeignKey(MealLog, related_name='members', on_delete=models.PROTECT)
    exercise_log = models.ForeignKey(ExerciseLog, related_name='members', on_delete=models.PROTECT)

    def __str__(self):
        return '%s' % self.last_name




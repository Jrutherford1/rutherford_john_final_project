from django.shortcuts import render

from calorie_counter.models import Member
from calorie_counter.models import DailyMacroGoal
from calorie_counter.models import Food
from calorie_counter.models import Meal
from calorie_counter.models import MealLog
from calorie_counter.models import Exercise
from calorie_counter.models import ExerciseLog
from calorie_counter.models import CalorieGoal



def member_list_view(request):
    member_list = Member.objects.all()
    # instructor_list = Instructor.objects.none()
    return render(request, 'calorie_counter/member_list.html', {'member_list': member_list})


def daily_macro_goal_list_view(request):
    daily_macro_goal_list = DailyMacroGoal.objects.all()
    # instructor_list = DailyMacroGoal.objects.none()
    return render(request, 'calorie_counter/daily_macro_goal_list.html', {'daily_macro_goal_list': daily_macro_goal_list})


def food_list_view(request):
    food_list = Food.objects.all()
    # instructor_list = Food.objects.none()
    return render(request, 'calorie_counter/food_list.html', {'food_list': food_list})


def meal_list_view(request):
    meal_list = Meal.objects.all()
    # instructor_list = Meal.objects.none()
    return render(request, 'calorie_counter/meal_list.html', {'meal_list': meal_list})


def meal_log_list_view(request):
    meal_log_list = MealLog.objects.all()
    # instructor_list = MealLog.objects.none()
    return render(request, 'calorie_counter/meal_log_list.html', {'meal_log_list': meal_log_list})


def exercise_list_view(request):
    exercise_list = Exercise.objects.all()
    # instructor_list = Exercise.objects.none()
    return render(request, 'calorie_counter/exercise_list.html', {'exercise_list': exercise_list})


def exercise_log_list_view(request):
    exercise_log_list = ExerciseLog.objects.all()
    # instructor_list = ExerciseLog.objects.none()
    return render(request, 'calorie_counter/exercise_log_list.html', {'exercise_log_list': exercise_log_list})


def calorie_goal_list_view(request):
    calorie_goal_list = CalorieGoal.objects.all()
    # instructor_list = CalorieGoal.objects.none()
    return render(request, 'calorie_counter/calorie_goal_list.html', {'calorie_goal_list': calorie_goal_list})



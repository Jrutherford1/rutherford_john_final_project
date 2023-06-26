from django.shortcuts import render
from django.views import View

from calorie_counter.models import Member
from calorie_counter.models import DailyMacroGoal
from calorie_counter.models import Food

from calorie_counter.models import MealLog
from calorie_counter.models import Exercise
from calorie_counter.models import ExerciseLog
from calorie_counter.models import CalorieGoal


class MemberList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/member_list.html',
            {'member_list': Member.objects.all()}
        )


class DailyMacroGoalList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/daily_macro_goal_list.html',
            {'daily_macro_goal_list': DailyMacroGoal.objects.all()}
        )


class FoodList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/food_list.html',
            {'food_list': Food.objects.all()}
        )


class MealList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/meal_list.html',
            {'meal_list': Meal.objects.all()}
        )


class MealLogList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/meal_log_list.html',
            {'meal_log_list': MealLog.objects.all()}
        )


class ExerciseList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/exercise_list.html',
            {'exercise_list': Exercise.objects.all()}
        )


class ExerciseLogList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/exercise_log_list.html',
            {'exercise_log_list': ExerciseLog.objects.all()}
        )


class CalorieGoalList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/calorie_goal_list.html',
            {'calorie_goal_list': CalorieGoal.objects.all()}
        )




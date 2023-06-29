from django.shortcuts import render, get_object_or_404
from django.views import View

from calorie_counter.models import Member
from calorie_counter.models import DailyMacroGoal
from calorie_counter.models import Food
from calorie_counter.models import MealLog
from calorie_counter.models import Exercise
from calorie_counter.models import ExerciseLog
from calorie_counter.models import CalorieGoal
from calorie_counter.models import MealFood


class MemberList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/member_list.html',
            {'member_list': Member.objects.all()}
        )


class MemberDetail(View):
    def get(self, request, pk):
        member_detail = get_object_or_404(Member, pk=pk)
        return render(
            request,
            'calorie_counter/member_detail.html',
            {'member_detail': member_detail,
             }
        )



class DailyMacroGoalList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/daily_macro_goal_list.html',
            {'daily_macro_goal_list': DailyMacroGoal.objects.all()}
        )

class DailyMacroGoalDetail(View):
    def get(self, request, pk):
        daily_macro_goal = get_object_or_404(DailyMacroGoal, pk=pk)
        return render(
            request,
            'calorie_counter/daily_macro_goal_detail.html',
            {'daily_macro_goal': daily_macro_goal,
             }
        )


class FoodList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/food_list.html',
            {'food_list': Food.objects.all()}
        )

class FoodDetail(View):
    def get(self, request, pk):
        food = get_object_or_404(Food, pk=pk)
        return render(
            request,
            'calorie_counter/food_detail.html',
            {'food': food,
             }
        )


class MealFoodList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/meal_food_list.html',
            {'meal_food_list': MealFood.objects.all()}
        )


class MealFoodDetail(View):
    def get(self, request, pk):
        meal_food_detail = get_object_or_404(MealFood, pk=pk)
        return render(
            request,
            'calorie_counter/meal_food_detail.html',
            {'meal_food_detail': meal_food_detail,
             }
        )


class MealLogList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/meal_log_list.html',
            {'meal_log_list': MealLog.objects.all()}
        )


class MealLogDetail(View):
    def get(self, request, pk):
        meal_log = get_object_or_404(MealLog, pk=pk)
        return render(
            request,
            'calorie_counter/meal_log_detail.html',
            {'meal_log': meal_log,
             }
        )


class ExerciseList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/exercise_list.html',
            {'exercise_list': Exercise.objects.all()}
        )


class ExerciseDetail(View):
    def get(self, request, pk):
        exercise = get_object_or_404(Exercise, pk=pk)
        return render(
            request,
            'calorie_counter/exercise_detail.html',
            {'exercise': exercise,
             }
        )


class ExerciseLogList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/exercise_log_list.html',
            {'exercise_log_list': ExerciseLog.objects.all()}
        )


class ExerciseLogDetail(View):
    def get(self, request, pk):
        exercise_log = get_object_or_404(ExerciseLog, pk=pk)
        return render(
            request,
            'calorie_counter/exercise_log_detail.html',
            {'exercise_log': exercise_log,
             }
        )


class CalorieGoalList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/calorie_goal_list.html',
            {'calorie_goal_list': CalorieGoal.objects.all()}
        )


class CalorieGoalDetail(View):
    def get(self, request, pk):
        calorie_goal = get_object_or_404(CalorieGoal, pk=pk)
        return render(
            request,
            'calorie_counter/calorie_goal_detail.html',
            {'calorie_goal': calorie_goal,
             }
        )



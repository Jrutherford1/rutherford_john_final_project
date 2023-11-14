from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy
from django.utils import timezone
from django.db import models


from calorie_counter.models import Member
from calorie_counter.models import DailyMacroGoal
from calorie_counter.models import Food
from calorie_counter.models import MealLog
from calorie_counter.models import Exercise
from calorie_counter.models import ExerciseLog
from calorie_counter.models import CalorieGoal
from calorie_counter.models import MealFood
from calorie_counter.utils import PageLinksMixin
from calorie_counter.forms import MemberForm
from calorie_counter.forms import DailyMacroGoalForm
from calorie_counter.forms import FoodForm
from calorie_counter.forms import MealLogForm
from calorie_counter.forms import ExerciseForm
from calorie_counter.forms import ExerciseLogForm
from calorie_counter.forms import CalorieGoalForm
from calorie_counter.forms import MealFoodForm


from django.views.generic import ListView, DetailView, CreateView,  UpdateView, DeleteView


class MemberList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):
    paginate_by = 25
    model = Member
    permission_required = 'calorie_counter.view_member'


class MemberDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Member
    template_name = 'calorie_counter/member_detail.html'
    permission_required = 'calorie_counter.view_member'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.get_object()
        context['member_detail'] = context.get('member')

        # Get today's date
        today = timezone.now().date()

        # Filter the member's meal logs and exercise logs by today's date
        meal_logs_today = member.meal_logs.filter(date=today)
        exercise_logs_today = member.exercise_logs.filter(date=today)

        # Calculate the total calories from today's meals and exercises
        total_calories_from_meals = sum(log.meal_foods.all().aggregate(
            total_calories=models.Sum(models.F('food__calories_per_serving') * models.F('quantity'),
                                      output_field=models.IntegerField()))['total_calories'] for log in meal_logs_today)
        total_calories_burned_from_exercises = sum(
            log.exercise.calories_burned_per_minute * log.duration for log in exercise_logs_today)

        # Calculate net calories
        net_calories = total_calories_from_meals - total_calories_burned_from_exercises

        # Update the context
        context['calorie_goals'] = member.calorie_goals.all()
        context['meal_logs'] = member.meal_logs.all()
        context['exercise_logs'] = member.exercise_logs.all()
        context['total_calories_from_meals_today'] = total_calories_from_meals
        context['total_calories_burned_from_exercises_today'] = total_calories_burned_from_exercises
        context['net_calories'] = net_calories

        return context


class MemberCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = MemberForm
    model = Member
    template_name = 'calorie_counter/member_form.html'
    permission_required = 'calorie_counter.add_member'


class MemberUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = MemberForm
    model = Member
    template_name = 'calorie_counter/member_form_update.html'
    permission_required = 'calorie_counter.change_member'


class MemberDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Member
    success_url = reverse_lazy('calorie_counter_member_list_urlpattern')
    permission_required = 'calorie_counter.delete_member'

    def get(self, request, pk):
        member = self.get_object()
        calorie_goals = member.calorie_goals.all()
        meal_logs = member.meal_logs.all()
        exercise_logs = member.exercise_logs.all()

        if calorie_goals.count() > 0 or meal_logs.count() > 0 or exercise_logs.count() > 0:
            return render(
                request,
                'calorie_counter/member_refuse_delete.html',
                {'member': member,
                 'calorie_goals': calorie_goals,
                 'meal_logs': meal_logs,
                 'exercise_logs': exercise_logs,
                 }
            )
        else:
            return render(
                request,
                'calorie_counter/member_confirm_delete.html',
                {'member': member}
            )


class DailyMacroGoalList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DailyMacroGoal
    template_name = 'calorie_counter/daily_macro_goal_list.html'
    context_object_name = 'daily_macro_goal_list'
    permission_required = 'calorie_counter.view_daily_macro_goal'


class DailyMacroGoalDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = DailyMacroGoal
    template_name = 'calorie_counter/daily_macro_goal_detail.html'
    context_object_name = 'daily_macro_goal_detail'
    permission_required = 'calorie_counter.view_daily_macro_goal'


class DailyMacroGoalCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = DailyMacroGoalForm
    model = DailyMacroGoal
    template_name = 'calorie_counter/daily_macro_goal_form.html'
    permission_required = 'calorie_counter.add_daily_macro_goal'


class DailyMacroGoalUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = DailyMacroGoal
    form_class = DailyMacroGoalForm
    template_name = 'calorie_counter/daily_macro_goal_form_update.html'
    context_object_name = 'daily_macro_goal'
    permission_required = 'calorie_counter.change_daily_macro_goal'


class DailyMacroGoalDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = DailyMacroGoal
    success_url = reverse_lazy('calorie_counter_daily_macro_goal_list_urlpattern')
    permission_required = 'calorie_counter.delete_daily_macro_goal'

    def get(self, request, pk):
        daily_macro_goal = self.get_object()
        return render(
            request,
            'calorie_counter/daily_macro_goal_confirm_delete.html',
            {'daily_macro_goal': daily_macro_goal}
        )


class FoodList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):
    paginate_by = 25
    model = Food
    permission_required = 'calorie_counter.view_food'


class FoodDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Food
    template_name = 'calorie_counter/food_detail.html'
    permission_required = 'calorie_counter.view_food'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['food_detail'] = context.get('food')
        return context


class FoodCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = FoodForm
    model = Food
    template_name = 'calorie_counter/food_form.html'
    permission_required = 'calorie_counter.add_food'


class FoodUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = FoodForm
    model = Food
    template_name = 'calorie_counter/food_form_update.html'
    permission_required = 'calorie_counter.change_food'


class FoodDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Food
    success_url = reverse_lazy('calorie_counter_food_list_urlpattern')
    permission_required = 'calorie_counter.delete_food'

    def get(self, request, pk):
        food = self.get_object()
        meal_foods = food.meal_foods.all()

        if meal_foods.count() > 0:
            return render(
                request,
                'calorie_counter/food_refuse_delete.html',
                {'food': food,
                 'meal_foods': meal_foods,
                 }
            )
        else:
            return render(
                request,
                'calorie_counter/food_confirm_delete.html',
                {'food': food}
            )


class MealFoodList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MealFood
    template_name = 'calorie_counter/meal_food_list.html'
    context_object_name = 'meal_food_list'
    permission_required = 'calorie_counter.view_meal_food'


class MealFoodDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MealFood
    template_name = 'calorie_counter/meal_food_detail.html'
    permission_required = 'calorie_counter.view_meal_food'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meal_food_detail'] = context.get('meal_food')
        return context


class MealFoodCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = MealFoodForm
    model = MealFood
    template_name = 'calorie_counter/meal_food_form.html'
    permission_required = 'calorie_counter.add_meal_food'


class MealFoodUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = MealFoodForm
    model = MealFood
    template_name = 'calorie_counter/meal_food_form_update.html'
    permission_required = 'calorie_counter.change_meal_food'


class MealFoodDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MealFood
    success_url = reverse_lazy('calorie_counter_meal_food_list_urlpattern')
    permission_required = 'calorie_counter.delete_meal_food'

    def get(self, request, pk):
        meal_food = self.get_object()
        return render(
            request,
            'calorie_counter/meal_food_confirm_delete.html',
            {'meal_food': meal_food}
        )


class MealLogList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MealLog
    template_name = 'calorie_counter/meal_log_list.html'
    context_object_name = 'meal_log_list'
    permission_required = 'calorie_counter.view_meal_log'


class MealLogDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MealLog
    template_name = 'calorie_counter/meal_log_detail.html'
    permission_required = 'calorie_counter.view_meal_log'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meal_log_detail'] = context.get('meal_log')
        return context


class MealLogCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = MealLogForm
    model = MealLog
    template_name = 'calorie_counter/meal_log_form.html'
    permission_required = 'calorie_counter.add_meal_log'


class MealLogUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = MealLogForm
    model = MealLog
    template_name = 'calorie_counter/meal_log_form_update.html'
    permission_required = 'calorie_counter.change_meal_log'


class MealLogDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MealLog
    success_url = reverse_lazy('calorie_counter_meal_log_list_urlpattern')
    permission_required = 'calorie_counter.delete_meal_log'

    def get(self, request, pk):
        meal_log = self.get_object()
        meal_foods = meal_log.meal_foods.all()
        permission_required = 'calorie_counter.delete_meal_log'

        if meal_foods.count() > 0:
            return render(
                request,
                'calorie_counter/meal_log_refuse_delete.html',
                {
                    'meal_log': meal_log,
                    'meal_foods': meal_foods,
                }
            )
        else:
            return render(
                request,
                'calorie_counter/meal_log_confirm_delete.html',
                {
                    'meal_log': meal_log,
                }
            )


class ExerciseList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Exercise
    template_name = 'calorie_counter/exercise_list.html'
    permission_required = 'calorie_counter.view_exercise'


class ExerciseDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Exercise
    template_name = 'calorie_counter/exercise_detail.html'
    context_object_name = 'exercise_detail'
    permission_required = 'calorie_counter.view_exercise'


class ExerciseCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = ExerciseForm
    model = Exercise
    template_name = 'calorie_counter/exercise_form.html'
    permission_required = 'calorie_counter.add_exercise'


class ExerciseUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = ExerciseForm
    model = Exercise
    template_name = 'calorie_counter/exercise_form_update.html'
    permission_required = 'calorie_counter.change_exercise'


class ExerciseDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Exercise
    success_url = reverse_lazy('calorie_counter_exercise_list_urlpattern')
    permission_required = 'calorie_counter.delete_exercise'

    def get(self, request, pk):
        exercise = self.get_object()
        exercise_logs = exercise.exercise_logs.all()

        if exercise_logs.count() > 0:
            return render(
                request,
                'calorie_counter/exercise_refuse_delete.html',
                {'exercise': exercise,
                 'exercise_logs': exercise_logs,
                 }
            )
        else:
            return render(
                request,
                'calorie_counter/exercise_confirm_delete.html',
                {'exercise': exercise}
            )


class ExerciseLogList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ExerciseLog
    template_name = 'calorie_counter/exercise_log_list.html'
    context_object_name = 'exercise_log_list'
    permission_required = 'calorie_counter.view_exercise_log'


class ExerciseLogDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = ExerciseLog
    template_name = 'calorie_counter/exercise_log_detail.html'
    context_object_name = 'exercise_log_detail'
    permission_required = 'calorie_counter.view_exercise_log'


class ExerciseLogCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = ExerciseLogForm
    model = ExerciseLog
    template_name = 'calorie_counter/exercise_log_form.html'
    permission_required = 'calorie_counter.add_exercise_log'


class ExerciseLogUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = ExerciseLogForm
    model = ExerciseLog
    template_name = 'calorie_counter/exercise_log_form_update.html'
    permission_required = 'calorie_counter.change_exercise_log'


class ExerciseLogDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ExerciseLog
    template_name = 'calorie_counter/exercise_log_confirm_delete.html'
    success_url = reverse_lazy('calorie_counter_exercise_log_list_urlpattern')
    permission_required = 'calorie_counter.delete_exercise_log'


class CalorieGoalList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CalorieGoal
    template_name = 'calorie_counter/calorie_goal_list.html'
    context_object_name = 'calorie_goal_list'
    permission_required = 'calorie_counter.view_calorie_goal'


class CalorieGoalDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = CalorieGoal
    template_name = 'calorie_counter/calorie_goal_detail.html'
    context_object_name = 'calorie_goal_detail'
    permission_required = 'calorie_counter.view_calorie_goal'


class CalorieGoalCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = CalorieGoalForm
    model = CalorieGoal
    template_name = 'calorie_counter/calorie_goal_form.html'
    permission_required = 'calorie_counter.add_calorie_goal'


class CalorieGoalUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = CalorieGoalForm
    model = CalorieGoal
    template_name = 'calorie_counter/calorie_goal_form_update.html'
    permission_required = 'calorie_counter.change_calorie_goal'


class CalorieGoalDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CalorieGoal
    template_name = 'calorie_counter/calorie_goal_confirm_delete.html'
    success_url = reverse_lazy('calorie_counter_calorie_goal_list_urlpattern')
    permission_required = 'calorie_counter.delete_calorie_goal'

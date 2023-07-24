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


class MemberList(PageLinksMixin, ListView):
    paginate_by = 25
    model = Member


# class MemberDetail(DetailView):
#     model = Member
#     template_name = 'calorie_counter/member_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         member = self.get_object()
#         context['member_detail'] = context.get('member')
#         context['calorie_goals'] = member.calorie_goals.all()
#         context['meal_logs'] = member.meal_logs.all()
#         context['exercise_logs'] = member.exercise_logs.all()
#         return context

class MemberDetail(DetailView):
    model = Member
    template_name = 'calorie_counter/member_detail.html'

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


class MemberCreate(CreateView):
    form_class = MemberForm
    model = Member
    template_name = 'calorie_counter/member_form.html'


class MemberUpdate(UpdateView):
    form_class = MemberForm
    model = Member
    template_name = 'calorie_counter/member_form_update.html'


class MemberDelete(DeleteView):
    model = Member
    success_url = reverse_lazy('calorie_counter_member_list_urlpattern')

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


class DailyMacroGoalList(ListView):
    model = DailyMacroGoal
    template_name = 'calorie_counter/daily_macro_goal_list.html'
    context_object_name = 'daily_macro_goal_list'


class DailyMacroGoalDetail(DetailView):
    model = DailyMacroGoal
    template_name = 'calorie_counter/daily_macro_goal_detail.html'
    context_object_name = 'daily_macro_goal_detail'


class DailyMacroGoalCreate(CreateView):
    form_class = DailyMacroGoalForm
    model = DailyMacroGoal
    template_name = 'calorie_counter/daily_macro_goal_form.html'


class DailyMacroGoalUpdate(UpdateView):
    model = DailyMacroGoal
    form_class = DailyMacroGoalForm
    template_name = 'calorie_counter/daily_macro_goal_form_update.html'
    context_object_name = 'daily_macro_goal'


class DailyMacroGoalDelete(DeleteView):
    model = DailyMacroGoal
    success_url = reverse_lazy('calorie_counter_daily_macro_goal_list_urlpattern')

    def get(self, request, pk):
        daily_macro_goal = self.get_object()
        return render(
            request,
            'calorie_counter/daily_macro_goal_confirm_delete.html',
            {'daily_macro_goal': daily_macro_goal}
        )


class FoodList(PageLinksMixin, ListView):
    paginate_by = 25
    model = Food


class FoodDetail(DetailView):
    model = Food
    template_name = 'calorie_counter/food_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['food_detail'] = context.get('food')
        return context


class FoodCreate(CreateView):
    form_class = FoodForm
    model = Food
    template_name = 'calorie_counter/food_form.html'


class FoodUpdate(UpdateView):
    form_class = FoodForm
    model = Food
    template_name = 'calorie_counter/food_form_update.html'


class FoodDelete(DeleteView):
    model = Food
    success_url = reverse_lazy('calorie_counter_food_list_urlpattern')

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


class MealFoodList(ListView):
    model = MealFood
    template_name = 'calorie_counter/meal_food_list.html'
    context_object_name = 'meal_food_list'


class MealFoodDetail(DetailView):
    model = MealFood
    template_name = 'calorie_counter/meal_food_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meal_food_detail'] = context.get('mealfood')
        return context


class MealFoodCreate(CreateView):
    form_class = MealFoodForm
    model = MealFood
    template_name = 'calorie_counter/meal_food_form.html'


class MealFoodUpdate(UpdateView):
    form_class = MealFoodForm
    model = MealFood
    template_name = 'calorie_counter/meal_food_form_update.html'


class MealFoodDelete(DeleteView):
    model = MealFood
    success_url = reverse_lazy('calorie_counter_meal_food_list_urlpattern')

    def get(self, request, pk):
        meal_food = self.get_object()
        return render(
            request,
            'calorie_counter/meal_food_confirm_delete.html',
            {'meal_food': meal_food}
        )


class MealLogList(ListView):
    model = MealLog
    template_name = 'calorie_counter/meal_log_list.html'
    context_object_name = 'meal_log_list'


class MealLogDetail(DetailView):
    model = MealLog
    template_name = 'calorie_counter/meal_log_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meal_log_detail'] = context.get('meallog')
        return context


class MealLogCreate(CreateView):
    form_class = MealLogForm
    model = MealLog
    template_name = 'calorie_counter/meal_log_form.html'


class MealLogUpdate(UpdateView):
    form_class = MealLogForm
    model = MealLog
    template_name = 'calorie_counter/meal_log_form_update.html'


class MealLogDelete(DeleteView):
    model = MealLog
    success_url = reverse_lazy('calorie_counter_meal_log_list_urlpattern')

    def get(self, request, pk):
        meal_log = self.get_object()
        meal_foods = meal_log.meal_foods.all()

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


class ExerciseList(ListView):
    model = Exercise
    template_name = 'calorie_counter/exercise_list.html'


class ExerciseDetail(DetailView):
    model = Exercise
    template_name = 'calorie_counter/exercise_detail.html'
    context_object_name = 'exercise_detail'


class ExerciseCreate(CreateView):
    form_class = ExerciseForm
    model = Exercise
    template_name = 'calorie_counter/exercise_form.html'


class ExerciseUpdate(UpdateView):
    form_class = ExerciseForm
    model = Exercise
    template_name = 'calorie_counter/exercise_form_update.html'


class ExerciseDelete(DeleteView):
    model = Exercise
    success_url = reverse_lazy('calorie_counter_exercise_list_urlpattern')

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


class ExerciseLogList(ListView):
    model = ExerciseLog
    template_name = 'calorie_counter/exercise_log_list.html'
    context_object_name = 'exercise_log_list'


class ExerciseLogDetail(DetailView):
    model = ExerciseLog
    template_name = 'calorie_counter/exercise_log_detail.html'
    context_object_name = 'exercise_log_detail'


class ExerciseLogCreate(CreateView):
    form_class = ExerciseLogForm
    model = ExerciseLog
    template_name = 'calorie_counter/exercise_log_form.html'


class ExerciseLogUpdate(UpdateView):
    form_class = ExerciseLogForm
    model = ExerciseLog
    template_name = 'calorie_counter/exercise_log_form_update.html'


class ExerciseLogDelete(View):

    def get(self, request, pk):
        exercise_log = self.get_object(pk)
        return render(
            request,
            'calorie_counter/exercise_log_confirm_delete.html',
            {'exercise_log': exercise_log}
        )

    def get_object(self, pk):
        exercise_log = get_object_or_404(
            ExerciseLog,
            pk=pk
        )
        return exercise_log

    def post(self, request, pk):
        exercise_log = self.get_object(pk)
        exercise_log.delete()
        return redirect('calorie_counter_exercise_log_list_urlpattern')


class CalorieGoalList(ListView):
    model = CalorieGoal
    template_name = 'calorie_counter/calorie_goal_list.html'
    context_object_name = 'calorie_goal_list'


class CalorieGoalDetail(DetailView):
    model = CalorieGoal
    template_name = 'calorie_counter/calorie_goal_detail.html'
    context_object_name = 'calorie_goal_detail'


class CalorieGoalCreate(CreateView):
    form_class = CalorieGoalForm
    model = CalorieGoal
    template_name = 'calorie_counter/calorie_goal_form.html'


class CalorieGoalUpdate(UpdateView):
    form_class = CalorieGoalForm
    model = CalorieGoal
    template_name = 'calorie_counter/calorie_goal_form_update.html'


class CalorieGoalDelete(View):

    def get(self, request, pk):
        calorie_goal = self.get_object(pk)
        return render(
            request,
            'calorie_counter/calorie_goal_confirm_delete.html',
            {'calorie_goal': calorie_goal}
        )

    def get_object(self, pk):
        calorie_goal = get_object_or_404(
            CalorieGoal,
            pk=pk
        )
        return calorie_goal

    def post(self, request, pk):
        calorie_goal = self.get_object(pk)
        calorie_goal.delete()
        return redirect('calorie_counter_calorie_goal_list_urlpattern')

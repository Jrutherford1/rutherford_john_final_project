from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from decimal import Decimal


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
    permission_required = 'calorie_counter.view_member'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.get_object()
        today = timezone.now().date()
        meal_logs_today = member.meallogs.filter(date=today)
        exercise_logs_today = member.exerciselogs.filter(date=today)
        total_protein = total_carbs = total_fat = total_calories_from_meals = 0

        for log in meal_logs_today:
            for mealfood in log.mealfoods.all():
                total_protein += mealfood.food.protein_grams * float(mealfood.quantity)
                total_carbs += mealfood.food.carbohydrates_grams * float(mealfood.quantity)
                total_fat += mealfood.food.fat_grams * float(mealfood.quantity)
                total_calories_from_meals += mealfood.food.calories_per_serving * float(mealfood.quantity)

        total_calories_burned_from_exercises = sum(
            log.exercise.calories_burned_per_minute * log.duration for log in exercise_logs_today)

        net_calories = Decimal(total_calories_from_meals) - total_calories_burned_from_exercises
        daily_macro_goal_today = DailyMacroGoal.objects.filter(member=member, date=today).first()

        if daily_macro_goal_today:
            net_protein = total_protein - daily_macro_goal_today.protein_goal
            net_carbs = total_carbs - daily_macro_goal_today.carbohydrate_goal
            net_fat = total_fat - daily_macro_goal_today.fat_goal
        else:
            net_protein = total_protein
            net_carbs = total_carbs
            net_fat = total_fat

        context['member_detail'] = member
        context['caloriegoals'] = member.caloriegoals.all()
        context['meallogs'] = member.meallogs.all()
        context['exerciselogs'] = member.exerciselogs.all()
        context['total_protein'] = total_protein
        context['total_carbs'] = total_carbs
        context['total_fat'] = total_fat
        context['total_calories_from_meals_today'] = total_calories_from_meals
        context['total_calories_burned_from_exercises_today'] = total_calories_burned_from_exercises
        context['net_calories'] = net_calories
        context['net_protein'] = net_protein
        context['net_carbs'] = net_carbs
        context['net_fat'] = net_fat

        return context


class MemberCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = MemberForm
    model = Member
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
        caloriegoals = member.caloriegoals.all()
        meallogs = member.meallogs.all()
        exerciselogs = member.exerciselogs.all()

        if caloriegoals.count() > 0 or meallogs.count() > 0 or exerciselogs.count() > 0:
            return render(
                request,
                'calorie_counter/member_refuse_delete.html',
                {'member': member,
                 'caloriegoals': caloriegoals,
                 'meallogs': meallogs,
                 'exerciselogs': exerciselogs,
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
    context_object_name = 'dailymacrogoal_list'
    permission_required = 'calorie_counter.view_dailymacrogoal'


class DailyMacroGoalDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = DailyMacroGoal
    context_object_name = 'dailymacrogoal_detail'
    permission_required = 'calorie_counter.view_dailymacrogoal'


class DailyMacroGoalCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = DailyMacroGoalForm
    model = DailyMacroGoal
    permission_required = 'calorie_counter.add_dailymacrogoal'


class DailyMacroGoalUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = DailyMacroGoal
    form_class = DailyMacroGoalForm
    template_name = 'calorie_counter/dailymacrogoal_form_update.html'
    context_object_name = 'dailymacrogoal'
    permission_required = 'calorie_counter.change_dailymacrogoal'


class DailyMacroGoalDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = DailyMacroGoal
    success_url = reverse_lazy('calorie_counter_dailymacrogoal_list_urlpattern')
    permission_required = 'calorie_counter.delete_dailymacrogoal'

    def get(self, request, pk):
        dailymacrogoal = self.get_object()
        return render(
            request,
            'calorie_counter/dailymacrogoal_confirm_delete.html',
            {'dailymacrogoal': dailymacrogoal}
        )


class FoodList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):
    paginate_by = 25
    model = Food
    permission_required = 'calorie_counter.view_food'


class FoodDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Food
    permission_required = 'calorie_counter.view_food'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['food_detail'] = context.get('food')
        return context


class FoodCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = FoodForm
    model = Food
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
        mealfoods = food.mealfoods.all()

        if mealfoods.count() > 0:
            return render(
                request,
                'calorie_counter/food_refuse_delete.html',
                {'food': food,
                 'mealfoods': mealfoods,
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
    context_object_name = 'mealfood_list'
    permission_required = 'calorie_counter.view_mealfood'


class MealFoodDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MealFood
    permission_required = 'calorie_counter.view_mealfood'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mealfood_detail'] = context.get('mealfood')
        return context


class MealFoodCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = MealFoodForm
    model = MealFood
    permission_required = 'calorie_counter.add_mealfood'


class MealFoodUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = MealFoodForm
    model = MealFood
    template_name = 'calorie_counter/mealfood_form_update.html'
    permission_required = 'calorie_counter.change_mealfood'


class MealFoodDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MealFood
    success_url = reverse_lazy('calorie_counter_mealfood_list_urlpattern')
    permission_required = 'calorie_counter.delete_mealfood'

    def get(self, request, pk):
        mealfood = self.get_object()
        return render(
            request,
            'calorie_counter/mealfood_confirm_delete.html',
            {'mealfood': mealfood}
        )


class MealLogList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MealLog
    context_object_name = 'meallog_list'
    permission_required = 'calorie_counter.view_meallog'


class MealLogDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MealLog
    permission_required = 'calorie_counter.view_meallog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meallog = self.object
        total_calories = sum(
            mealfood.food.calories_per_serving * float(mealfood.quantity) for mealfood in meallog.mealfoods.all())

        context['meallog_detail'] = meallog
        context['total_calories'] = total_calories

        return context


class MealLogCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = MealLogForm
    model = MealLog
    permission_required = 'calorie_counter.add_meallog'


class MealLogUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = MealLogForm
    model = MealLog
    template_name = 'calorie_counter/meallog_form_update.html'
    permission_required = 'calorie_counter.change_meallog'


class MealLogDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MealLog
    success_url = reverse_lazy('calorie_counter_meallog_list_urlpattern')
    permission_required = 'calorie_counter.delete_meallog'

    def get(self, request, pk):
        meallog = self.get_object()
        mealfoods = meallog.mealfoods.all()

        if mealfoods.count() > 0:
            return render(
                request,
                'calorie_counter/meallog_refuse_delete.html',
                {
                    'meallog': meallog,
                    'mealfoods': mealfoods,
                }
            )
        else:
            return render(
                request,
                'calorie_counter/meallog_confirm_delete.html',
                {
                    'meallog': meallog,
                }
            )


class ExerciseList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Exercise
    permission_required = 'calorie_counter.view_exercise'


class ExerciseDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Exercise
    context_object_name = 'exercise_detail'
    permission_required = 'calorie_counter.view_exercise'


class ExerciseCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = ExerciseForm
    model = Exercise
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
        exerciselogs = exercise.exerciselogs.all()

        if exerciselogs.count() > 0:
            return render(
                request,
                'calorie_counter/exercise_refuse_delete.html',
                {'exercise': exercise,
                 'exerciselogs': exerciselogs,
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
    context_object_name = 'exerciselog_list'
    permission_required = 'calorie_counter.view_exerciselog'


class ExerciseLogDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = ExerciseLog
    permission_required = 'calorie_counter.view_exerciselog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exerciselog = self.object

        total_calories_burned = exerciselog.exercise.calories_burned_per_minute * float(exerciselog.duration)

        context['exerciselog_detail'] = exerciselog
        context['total_calories_burned'] = total_calories_burned

        return context


class ExerciseLogCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = ExerciseLogForm
    model = ExerciseLog
    permission_required = 'calorie_counter.add_exerciselog'


class ExerciseLogUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = ExerciseLogForm
    model = ExerciseLog
    template_name = 'calorie_counter/exerciselog_form_update.html'
    permission_required = 'calorie_counter.change_exerciselog'


class ExerciseLogDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ExerciseLog
    success_url = reverse_lazy('calorie_counter_exerciselog_list_urlpattern')
    permission_required = 'calorie_counter.delete_exerciselog'


class CalorieGoalList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CalorieGoal
    context_object_name = 'caloriegoal_list'
    permission_required = 'calorie_counter.view_caloriegoal'


class CalorieGoalDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = CalorieGoal
    context_object_name = 'caloriegoal_detail'
    permission_required = 'calorie_counter.view_caloriegoal'


class CalorieGoalCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = CalorieGoalForm
    model = CalorieGoal
    permission_required = 'calorie_counter.add_caloriegoal'


class CalorieGoalUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = CalorieGoalForm
    model = CalorieGoal
    template_name = 'calorie_counter/caloriegoal_form_update.html'
    permission_required = 'calorie_counter.change_caloriegoal'


class CalorieGoalDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CalorieGoal
    success_url = reverse_lazy('calorie_counter_caloriegoal_list_urlpattern')
    permission_required = 'calorie_counter.delete_caloriegoal'

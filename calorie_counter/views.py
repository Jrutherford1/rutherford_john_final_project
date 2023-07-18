from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy


from calorie_counter.models import Member
from calorie_counter.models import DailyMacroGoal
from calorie_counter.models import Food
from calorie_counter.models import MealLog
from calorie_counter.models import Exercise
from calorie_counter.models import ExerciseLog
from calorie_counter.models import CalorieGoal
from calorie_counter.models import MealFood
from calorie_counter.utils import ObjectCreateMixin, PageLinksMixin
from calorie_counter.forms import MemberForm
from calorie_counter.forms import DailyMacroGoalForm
from calorie_counter.forms import FoodForm
from calorie_counter.forms import MealLogForm
from calorie_counter.forms import ExerciseForm
from calorie_counter.forms import ExerciseLogForm
from calorie_counter.forms import CalorieGoalForm
from calorie_counter.forms import MealFoodForm


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class MemberList(PageLinksMixin, ListView):
    paginate_by = 25
    model = Member


class MemberDetail(DetailView):
    model = Member
    template_name = 'calorie_counter/member_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.get_object()
        context['member_detail'] = context.get('member')
        context['calorie_goals'] = member.calorie_goals.all()
        context['meal_logs'] = member.meal_logs.all()
        context['exercise_logs'] = member.exercise_logs.all()
        return context


class MemberCreate(ObjectCreateMixin, View):
    form_class = MemberForm
    template_name = 'calorie_counter/member_form.html'


class MemberUpdate(View):
    form_class = MemberForm
    model = Member
    template_name = 'calorie_counter/member_form_update.html'

    def get_object(self, pk):
        return get_object_or_404(
            self.model,
            pk=pk)

    def get(self, request, pk):
        member = self.get_object(pk)
        context = {
            'form': self.form_class(
                instance=member),
            'member': member,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, pk):
        member = self.get_object(pk)
        bound_form = self.form_class(
            request.POST, instance=member)
        if bound_form.is_valid():
            new_member = bound_form.save()
            return redirect(new_member)
        else:
            context = {
                'form': bound_form,
                'member': member,
            }
            return render(
                request,
                self.template_name,
                context)


class MemberDelete(View):

    def get(self, request, pk):
        member = self.get_object(pk)
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

    def get_object(self, pk):
        member = get_object_or_404(
            Member,
            pk=pk
        )
        return member

    def post(self, request, pk):
        member = self.get_object(pk)
        member.delete()
        return redirect('calorie_counter_member_list_urlpattern')


class DailyMacroGoalList(ListView):
    model = DailyMacroGoal
    template_name = 'calorie_counter/daily_macro_goal_list.html'
    context_object_name = 'daily_macro_goal_list'


class DailyMacroGoalDetail(DetailView):
    model = DailyMacroGoal
    template_name = 'calorie_counter/daily_macro_goal_detail.html'
    context_object_name = 'daily_macro_goal_detail'


class DailyMacroGoalCreate(ObjectCreateMixin, View):
    form_class = DailyMacroGoalForm
    template_name = 'calorie_counter/daily_macro_goal_form.html'


class DailyMacroGoalUpdate(View):
    form_class = DailyMacroGoalForm
    model = DailyMacroGoal
    template_name = 'calorie_counter/daily_macro_goal_form_update.html'

    def get_object(self, pk):
        return get_object_or_404(
            self.model,
            pk=pk)

    def get(self, request, pk):
        daily_macro_goal = self.get_object(pk)
        context = {
            'form': self.form_class(
                instance=daily_macro_goal),
            'daily_macro_goal': daily_macro_goal,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, pk):
        daily_macro_goal = self.get_object(pk)
        bound_form = self.form_class(
            request.POST, instance=daily_macro_goal)
        if bound_form.is_valid():
            new_daily_macro_goal = bound_form.save()
            return redirect(new_daily_macro_goal)
        else:
            context = {
                'form': bound_form,
                'daily_macro_goal': daily_macro_goal,
            }
            return render(
                request,
                self.template_name,
                context)


class DailyMacroGoalDelete(View):

    def get(self, request, pk):
        daily_macro_goal = self.get_object(pk)
        return render(
            request,
            'calorie_counter/daily_macro_goal_confirm_delete.html',
            {'daily_macro_goal': daily_macro_goal}
        )

    def get_object(self, pk):
        daily_macro_goal = get_object_or_404(
            DailyMacroGoal,
            pk=pk
        )
        return daily_macro_goal

    def post(self, request, pk):
        daily_macro_goal = self.get_object(pk)
        daily_macro_goal.delete()
        return redirect('calorie_counter_daily_macro_goal_list_urlpattern')


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


class FoodCreate(ObjectCreateMixin, View):
    form_class = FoodForm
    template_name = 'calorie_counter/food_form.html'


class FoodUpdate(View):
    form_class = FoodForm
    model = Food
    template_name = 'calorie_counter/food_form_update.html'

    def get_object(self, pk):
        return get_object_or_404(
            self.model,
            pk=pk)

    def get(self, request, pk):
        food = self.get_object(pk)
        context = {
            'form': self.form_class(
                instance=food),
            'food': food,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, pk):
        food = self.get_object(pk)
        bound_form = self.form_class(
            request.POST, instance=food)
        if bound_form.is_valid():
            new_food = bound_form.save()
            return redirect(new_food)
        else:
            context = {
                'form': bound_form,
                'food': food,
            }
            return render(
                request,
                self.template_name,
                context)


class FoodDelete(View):

    def get(self, request, pk):
        food = self.get_object(pk)
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

    def get_object(self, pk):
        return get_object_or_404(
            Food,
            pk=pk)

    def post(self, request, pk):
        food = self.get_object(pk)
        food.delete()
        return redirect('calorie_counter_food_list_urlpattern')


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


class MealFoodCreate(ObjectCreateMixin, View):
    form_class = MealFoodForm
    template_name = 'calorie_counter/meal_food_form.html'


class MealFoodUpdate(View):
    form_class = MealFoodForm
    model = MealFood
    template_name = 'calorie_counter/meal_food_form_update.html'

    def get_object(self, pk):
        return get_object_or_404(
            self.model,
            pk=pk)

    def get(self, request, pk):
        meal_food = self.get_object(pk)
        context = {
            'form': self.form_class(
                instance=meal_food),
            'meal_food': meal_food,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, pk):
        meal_food = self.get_object(pk)
        bound_form = self.form_class(
            request.POST, instance=meal_food)
        if bound_form.is_valid():
            new_meal_food = bound_form.save()
            return redirect(new_meal_food)
        else:
            context = {
                'form': bound_form,
                'meal_food': meal_food,
            }
            return render(
                request,
                self.template_name,
                context)


class MealFoodDelete(View):
    def get(self, request, pk):
        meal_food = self.get_object(pk)

        # Get related MealLog and Food
        meal_log = meal_food.meal_log
        food = meal_food.food

        # Check if MealFood is associated with a MealLog
        if meal_log is not None:
            return render(
                request,
                'calorie_counter/meal_food_refuse_delete.html',
                {
                    'meal_food': meal_food,
                    'meal_log': meal_log,
                    'food': food,
                }
            )
        else:
            return render(
                request,
                'calorie_counter/meal_food_confirm_delete.html',
                {
                    'meal_food': meal_food,
                }
            )

    def get_object(self, pk):
        return get_object_or_404(
            MealFood,
            pk=pk
        )

    def post(self, request, pk):
        meal_food = self.get_object(pk)
        meal_food.delete()
        return redirect('calorie_counter_meal_food_list_urlpattern')


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


class MealLogCreate(ObjectCreateMixin, View):
    form_class = MealLogForm
    template_name = 'calorie_counter/meal_log_form.html'


class MealLogUpdate(View):
    form_class = MealLogForm
    model = MealLog
    template_name = 'calorie_counter/meal_log_form_update.html'

    def get_object(self, pk):
        return get_object_or_404(
            self.model,
            pk=pk)

    def get(self, request, pk):
        meal_log = self.get_object(pk)
        context = {
            'form': self.form_class(
                instance=meal_log),
            'meal_log': meal_log,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, pk):
        meal_log = self.get_object(pk)
        bound_form = self.form_class(
            request.POST, instance=meal_log)
        if bound_form.is_valid():
            new_meal_log = bound_form.save()
            return redirect(new_meal_log)
        else:
            context = {
                'form': bound_form,
                'meal_log': meal_log,
            }
            return render(
                request,
                self.template_name,
                context)


class MealLogDelete(View):
    def get(self, request, pk):
        meal_log = self.get_object(pk)
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

    def get_object(self, pk):
        return get_object_or_404(
            MealLog,
            pk=pk
        )

    def post(self, request, pk):
        meal_log = self.get_object(pk)
        meal_log.delete()
        return redirect('calorie_counter_meal_log_list_urlpattern')


class ExerciseList(ListView):
    model = Exercise
    template_name = 'calorie_counter/exercise_list.html'


class ExerciseDetail(DetailView):
    model = Exercise
    template_name = 'calorie_counter/exercise_detail.html'
    context_object_name = 'exercise_detail'


class ExerciseCreate(ObjectCreateMixin, View):
    form_class = ExerciseForm
    template_name = 'calorie_counter/exercise_form.html'


class ExerciseUpdate(View):
    form_class = ExerciseForm
    model = Exercise
    template_name = 'calorie_counter/exercise_form_update.html'

    def get_object(self, pk):
        return get_object_or_404(
            self.model,
            pk=pk)

    def get(self, request, pk):
        exercise = self.get_object(pk)
        context = {
            'form': self.form_class(
                instance=exercise),
            'exercise': exercise,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, pk):
        exercise = self.get_object(pk)
        bound_form = self.form_class(
            request.POST, instance=exercise)
        if bound_form.is_valid():
            new_exercise = bound_form.save()
            return redirect(new_exercise)
        else:
            context = {
                'form': bound_form,
                'exercise': exercise,
            }
            return render(
                request,
                self.template_name,
                context)


class ExerciseDelete(View):
    def get(self, request, pk):
        exercise = self.get_object(pk)
        exercise_logs = exercise.exercise_logs.all()

        if exercise_logs.count() > 0:
            return render(
                request,
                'calorie_counter/exercise_refuse_delete.html',
                {
                    'exercise': exercise,
                    'exercise_logs': exercise_logs,
                }
            )
        else:
            return render(
                request,
                'calorie_counter/exercise_confirm_delete.html',
                {
                    'exercise': exercise,
                }
            )

    def get_object(self, pk):
        return get_object_or_404(
            Exercise,
            pk=pk
        )

    def post(self, request, pk):
        exercise = self.get_object(pk)
        exercise.delete()
        return redirect('calorie_counter_exercise_list_urlpattern')


class ExerciseLogList(ListView):
    model = ExerciseLog
    template_name = 'calorie_counter/exercise_log_list.html'
    context_object_name = 'exercise_log_list'


class ExerciseLogDetail(DetailView):
    model = ExerciseLog
    template_name = 'calorie_counter/exercise_log_detail.html'
    context_object_name = 'exercise_log_detail'


class ExerciseLogCreate(ObjectCreateMixin, View):
    form_class = ExerciseLogForm
    template_name = 'calorie_counter/exercise_log_form.html'


class ExerciseLogUpdate(View):
    form_class = ExerciseLogForm
    model = ExerciseLog
    template_name = 'calorie_counter/exercise_log_form_update.html'

    def get_object(self, pk):
        return get_object_or_404(
            self.model,
            pk=pk)

    def get(self, request, pk):
        exercise_log = self.get_object(pk)
        context = {
            'form': self.form_class(
                instance=exercise_log),
            'exercise_log': exercise_log,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, pk):
        exercise_log = self.get_object(pk)
        bound_form = self.form_class(
            request.POST, instance=exercise_log)
        if bound_form.is_valid():
            new_exercise_log = bound_form.save()
            return redirect(new_exercise_log)
        else:
            context = {
                'form': bound_form,
                'exercise_log': exercise_log,
            }
            return render(
                request,
                self.template_name,
                context)


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


class CalorieGoalCreate(ObjectCreateMixin, View):
    form_class = CalorieGoalForm
    template_name = 'calorie_counter/calorie_goal_form.html'


class CalorieGoalUpdate(View):
    form_class = CalorieGoalForm
    model = CalorieGoal
    template_name = 'calorie_counter/calorie_goal_form_update.html'

    def get_object(self, pk):
        return get_object_or_404(
            self.model,
            pk=pk)

    def get(self, request, pk):
        calorie_goal = self.get_object(pk)
        context = {
            'form': self.form_class(
                instance=calorie_goal),
            'calorie_goal': calorie_goal,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, pk):
        calorie_goal = self.get_object(pk)
        bound_form = self.form_class(
            request.POST, instance=calorie_goal)
        if bound_form.is_valid():
            new_calorie_goal = bound_form.save()
            return redirect(new_calorie_goal)
        else:
            context = {
                'form': bound_form,
                'calorie_goal': calorie_goal,
            }
            return render(
                request,
                self.template_name,
                context)


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

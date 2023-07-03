from django.shortcuts import render, get_object_or_404, redirect
from django.views import View


from calorie_counter.models import Member
from calorie_counter.models import DailyMacroGoal
from calorie_counter.models import Food
from calorie_counter.models import MealLog
from calorie_counter.models import Exercise
from calorie_counter.models import ExerciseLog
from calorie_counter.models import CalorieGoal
from calorie_counter.models import MealFood
from calorie_counter.utils import ObjectCreateMixin
from calorie_counter.forms import MemberForm
from calorie_counter.forms import DailyMacroGoalForm
from calorie_counter.forms import FoodForm
from calorie_counter.forms import MealLogForm
from calorie_counter.forms import ExerciseForm
from calorie_counter.forms import ExerciseLogForm
from calorie_counter.forms import CalorieGoalForm
from calorie_counter.forms import MealFoodForm


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




class DailyMacroGoalList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/daily_macro_goal_list.html',
            {'daily_macro_goal_list': DailyMacroGoal.objects.all()}
        )


class DailyMacroGoalDetail(View):
    def get(self, request, pk):
        daily_macro_goal_detail = get_object_or_404(DailyMacroGoal, pk=pk)
        return render(
            request,
            'calorie_counter/daily_macro_goal_detail.html',
            {'daily_macro_goal_detail': daily_macro_goal_detail,
             }
        )


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


class FoodList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/food_list.html',
            {'food_list': Food.objects.all()}
        )

class FoodDetail(View):
    def get(self, request, pk):
        food_detail = get_object_or_404(Food, pk=pk)
        return render(
            request,
            'calorie_counter/food_detail.html',
            {'food_detail': food_detail,
             }
        )

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


class MealLogList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/meal_log_list.html',
            {'meal_log_list': MealLog.objects.all()}
        )


class MealLogDetail(View):
    def get(self, request, pk):
        meal_log_detail = get_object_or_404(MealLog, pk=pk)
        return render(
            request,
            'calorie_counter/meal_log_detail.html',
            {'meal_log_detail': meal_log_detail,
             }
        )


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


class ExerciseList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/exercise_list.html',
            {'exercise_list': Exercise.objects.all()}
        )


class ExerciseDetail(View):
    def get(self, request, pk):
        exercise_detail = get_object_or_404(Exercise, pk=pk)
        return render(
            request,
            'calorie_counter/exercise_detail.html',
            {'exercise_detail': exercise_detail,
             }
        )


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


class ExerciseLogList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/exercise_log_list.html',
            {'exercise_log_list': ExerciseLog.objects.all()}
        )


class ExerciseLogDetail(View):
    def get(self, request, pk):
        exercise_log_detail = get_object_or_404(ExerciseLog, pk=pk)
        return render(
            request,
            'calorie_counter/exercise_log_detail.html',
            {'exercise_log_detail': exercise_log_detail,
             }
        )


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


class CalorieGoalList(View):

    def get(self, request):
        return render(
            request,
            'calorie_counter/calorie_goal_list.html',
            {'calorie_goal_list': CalorieGoal.objects.all()}
        )


class CalorieGoalDetail(View):
    def get(self, request, pk):
        calorie_goal_detail = get_object_or_404(CalorieGoal, pk=pk)
        return render(
            request,
            'calorie_counter/calorie_goal_detail.html',
            {'calorie_goal_detail': calorie_goal_detail,
             }
        )


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

from django import forms
from calorie_counter.models import Member
from calorie_counter.models import DailyMacroGoal
from calorie_counter.models import Food
from calorie_counter.models import MealLog
from calorie_counter.models import Exercise
from calorie_counter.models import ExerciseLog
from calorie_counter.models import CalorieGoal
from calorie_counter.models import MealFood


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

        def clean_first_name(self):
            return self.cleaned_data['first_name'].strip()

        def clean_last_name(self):
            return self.cleaned_data['last_name'].strip()

        def clean_disambiguator(self):
            if len(self.cleaned_data['disambiguator']) == 0:
                result = self.cleaned_data['disambiguator']
            else:
                result = self.cleaned_data['disambiguator'].strip()
            return result


class DailyMacroGoalForm(forms.ModelForm):
    class Meta:
        model = DailyMacroGoal
        fields = '__all__'

        def clean_member(self):
            return self.cleaned_data['member'].strip()

        def clean_protein_goal(self):
            return self.cleaned_data['protein_goal'].strip()

        def clean_carbohydrate_goal(self):
            return self.cleaned_data['carbohydrate_goal'].strip()

        def clean_fat_goal(self):
            return self.cleaned_data['fat_goal'].strip()

        def clean_date(self):
            return self.cleaned_data['date'].strip()


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'

        def clean_name(self):
            return self.cleaned_data['name'].strip()

        def clean_calories_per_serving(self):
            return self.cleaned_data['calories_per_serving'].strip()

        def clean_protein_grams(self):
            return self.cleaned_data['protein_grams'].strip()

        def clean_carbohydrate_grams(self):
            return self.cleaned_data['carbohydrate_grams'].strip()

        def clean_fat_grams(self):
            return self.cleaned_data['fat_grams'].strip()


class MealFoodForm(forms.ModelForm):
    class Meta:
        model = MealFood
        fields = '__all__'

        def clean_meal_log(self):
            return self.cleaned_data['meallog'].strip()

        def clean_food(self):
            return self.cleaned_data['food'].strip()

        def clean_quantity(self):
            return self.cleaned_data['quantity'].strip()


class MealLogForm(forms.ModelForm):
    class Meta:
        model = MealLog
        fields = '__all__'

        def clean_member(self):
            return self.cleaned_data['member'].strip()

        def clean_date(self):
            return self.cleaned_data['date'].strip()

        def clean_time(self):
            return self.cleaned_data['time'].strip()

        def clean_meal_type(self):
            return self.cleaned_data['meal_type'].strip()


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = '__all__'

        def clean_exercise_type(self):
            return self.cleaned_data['exercise_type'].strip()

        def clean_exercise_category(self):
            return self.cleaned_data['exercise_category'].strip()

        def clean_calories_burned_per_minute(self):
            return self.cleaned_data['calories_burned_per_minute'].strip()


class ExerciseLogForm(forms.ModelForm):
    class Meta:
        model = ExerciseLog
        fields = '__all__'

        def clean_member(self):
            return self.cleaned_data['member'].strip()

        def clean_date(self):
            return self.cleaned_data['date'].strip()

        def clean_duration(self):
            return self.cleaned_data['duration'].strip()

        def clean_exercise(self):
            return self.cleaned_data['exercise'].strip()


class CalorieGoalForm(forms.ModelForm):
    class Meta:
        model = CalorieGoal
        fields = '__all__'

        def clean_member(self):
            return self.cleaned_data['member'].strip()

        def clean_target_calories(self):
            return self.cleaned_data['target_calories'].strip()

        def clean_begin_date(self):
            return self.cleaned_data['begin_date'].strip()

        def clean_end_date(self):
            return self.cleaned_data['end_date'].strip()

from django.contrib import admin

from .models import Member
from .models import DailyMacroGoal
from .models import Food
from .models import Meal
from .models import MealLog
from .models import Exercise
from .models import ExerciseLog
from .models import CalorieGoal


admin.site.register(Member)
admin.site.register(DailyMacroGoal)
admin.site.register(Food)
admin.site.register(Meal)
admin.site.register(MealLog)
admin.site.register(Exercise)
admin.site.register(ExerciseLog)
admin.site.register(CalorieGoal)


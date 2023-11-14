from django.contrib import admin

from .models import Member
from .models import DailyMacroGoal
from .models import Food
from .models import MealLog
from .models import Exercise
from .models import ExerciseLog
from .models import CalorieGoal
from .models import MealFood


admin.site.register(Member)
admin.site.register(DailyMacroGoal)
admin.site.register(Food)
admin.site.register(MealLog)
admin.site.register(Exercise)
admin.site.register(ExerciseLog)
admin.site.register(CalorieGoal)
admin.site.register(MealFood)


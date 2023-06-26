"""rutherford_john_final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from calorie_counter.views import (
    FoodList,
    MemberList,
    MealList,
    MealLogList,
    ExerciseLogList,
    DailyMacroGoalList,
    CalorieGoalList,
    ExerciseList,
)

urlpatterns = [
    path('member/',
             MemberList.as_view(),
             name='calorie_counter_member_list_urlpattern'),

    path('food/',
             FoodList.as_view(),
             name='calorie_counter_food_list_urlpattern'),



    path('meallog/',
             MealLogList.as_view(),
             name='calorie_counter_meallog_list_urlpattern'),

    path('exerciselog/',
             ExerciseLogList.as_view(),
             name='calorie_counter_exerciselog_list_urlpattern'),

    path('dailymacrogoal/',
             DailyMacroGoalList.as_view(),
             name='calorie_counter_dailymacrogoal_list_urlpattern'),

    path('caloriegoal/',
             CalorieGoalList.as_view(),
             name='calorie_counter_caloriegoal_list_urlpattern'),

    path('exercise/',
             ExerciseList.as_view(),
             name='calorie_counter_exercise_list_urlpattern'),
   ]
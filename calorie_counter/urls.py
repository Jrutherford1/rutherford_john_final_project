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
    member_list_view, food_list_view, meal_list_view, meal_log_list_view, exercise_log_list_view,
    calorie_goal_list_view, exercise_list_view, daily_macro_goal_list_view,
)

urlpatterns = [
    path('member/', member_list_view, name='member_list'),
    path('food/', food_list_view, name='food_list'),
    path('meal/', meal_list_view, name='meal_list'),
    path('meallog/', meal_log_list_view, name='meal_log_list'),
    path('exerciselog/', exercise_log_list_view, name='exercise_log_list'),
    path('dailymacrogoal/', daily_macro_goal_list_view, name='daily_macro_goal_list'),
    path('caloriegoal/', calorie_goal_list_view, name='calorie_goal_list'),
    path('exercise/', exercise_list_view, name='exercise_list'),


]
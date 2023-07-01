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
    MealFoodList,
    MealLogList,
    ExerciseLogList,
    DailyMacroGoalList,
    CalorieGoalList,
    ExerciseList,
    MemberDetail,
    MealLogDetail,
    FoodDetail,
    ExerciseLogDetail,
    MealFoodDetail,
    ExerciseDetail,
    DailyMacroGoalDetail,
    CalorieGoalDetail,
    MemberCreate,
    FoodCreate,
    MealLogCreate,



)

urlpatterns = [
    path('member/',
             MemberList.as_view(),
             name='calorie_counter_member_list_urlpattern'),

    path('member/<int:pk>/',
            MemberDetail.as_view(),
            name='calorie_counter_member_detail_urlpattern'),

    path('member/create/',
            MemberCreate.as_view(),
            name='calorie_counter_member_create_urlpattern'),

    path('food/',
             FoodList.as_view(),
             name='calorie_counter_food_list_urlpattern'),

    path('food/<int:pk>/',
                FoodDetail.as_view(),
                name='calorie_counter_food_detail_urlpattern'),

    path('food/create/',
            FoodCreate.as_view(),
            name='calorie_counter_food_create_urlpattern'),

    path('meallog/',
             MealLogList.as_view(),
             name='calorie_counter_meal_log_list_urlpattern'),

    path('meallog/<int:pk>/',
            MealLogDetail.as_view(),
            name='calorie_counter_meal_log_detail_urlpattern'),

    path('meallog/create/',
            MealLogCreate.as_view(),
            name='calorie_counter_meal_log_create_urlpattern'),

    path('exerciselog/',
             ExerciseLogList.as_view(),
             name='calorie_counter_exercise_log_list_urlpattern'),

    path('exerciselog/<int:pk>/',
            ExerciseLogDetail.as_view(),
            name='calorie_counter_exercise_log_detail_urlpattern'),

    path('exercise/create/',
            ExerciseCreate.as_view(),
            name='calorie_counter_exercise_create_urlpattern'),

    path('dailymacrogoal/',
             DailyMacroGoalList.as_view(),
             name='calorie_counter_daily_macro_goal_list_urlpattern'),

    path('dailymacrogoal/<int:pk>/',
            DailyMacroGoalDetail.as_view(),
            name='calorie_counter_daily_macro_goal_detail_urlpattern'),

    path('dailymacrogoal/create/',
            DailyMacroGoalCreate.as_view(),
            name='calorie_counter_daily_macro_goal_create_urlpattern'),

    path('caloriegoal/',
             CalorieGoalList.as_view(),
             name='calorie_counter_calorie_goal_list_urlpattern'),

    path('caloriegoal/<int:pk>/',
            CalorieGoalDetail.as_view(),
            name='calorie_counter_calorie_goal_detail_urlpattern'),

    path('caloriegoal/create/',
            CalorieGoalCreate.as_view(),
            name='calorie_counter_calorie_goal_create_urlpattern'),

    path('exercise/',
             ExerciseList.as_view(),
             name='calorie_counter_exercise_list_urlpattern'),

    path('exercise/<int:pk>/',
            ExerciseDetail.as_view(),
            name='calorie_counter_exercise_detail_urlpattern'),

    path('exercise/create/',
            ExerciseCreate.as_view(),
            name='calorie_counter_exercise_create_urlpattern'),

    path('mealfood/',
             MealFoodList.as_view(),
             name='calorie_counter_mealfood_list_urlpattern'),

    path('mealfood/<int:pk>/',
            MealFoodDetail.as_view(),
            name='calorie_counter_meal_food_detail_urlpattern'),

    path('mealfood/create/',
            MealFoodCreate.as_view(),
            name='calorie_counter_meal_food_create_urlpattern'),
   ]
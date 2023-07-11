from django.shortcuts import redirect


def redirect_root_view(request):
    return redirect("calorie_counter_meal_log_list_urlpattern")

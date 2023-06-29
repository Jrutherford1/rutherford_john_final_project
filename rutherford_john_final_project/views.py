from django.shortcuts import redirect


def redirect_root_view(request):
    return redirect("calorie_counter_member_list_urlpattern")

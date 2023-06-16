from django.shortcuts import render

from calorie_counter.models import Member


def member_list_view(request):
    member_list = Member.objects.all()
    # instructor_list = Instructor.objects.none()
    return render(request, 'calorie_counter/member_list.html', {'member_list': member_list})
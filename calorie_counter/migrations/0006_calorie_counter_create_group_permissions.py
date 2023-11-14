from __future__ import unicode_literals
from itertools import chain

from django.db import migrations

def populate_permissions_lists(apps):
    permission_class = apps.get_model('auth', 'Permission')

    member_permissions = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                             content_type__model='member')

    daily_macro_goal_permissions = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                          content_type__model='daily_macro_goal')

    food_permissions = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                                  content_type__model='food')

    meal_food_permissions = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                                  content_type__model='meal_food')

    meal_log_permissions = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                           content_type__model='meal_log')

    exercise_permissions = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                         content_type__model='exercise')

    exercise_log_permissions = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                          content_type__model='exercise_log')

    calorie_goal_permissions = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                               content_type__model='calorie_goal')

    perm_view_member = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                           content_type__model='member',
                                                           codename='view_member')

    perm_view_daily_macro_goal = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                        content_type__model='daily_macro_goal',
                                                        codename='view_daily_macro_goal')

    perm_view_food = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                               content_type__model='food',
                                                               codename='view_food')

    perm_view_meal_food = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                               content_type__model='meal_food',
                                                               codename='view_meal_food')

    perm_view_meal_log = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                         content_type__model='meal_log',
                                                         codename='view_meal_log')

    perm_view_exercise = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                       content_type__model='exercise',
                                                       codename='view_exercise')

    perm_view_exercise_log = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                        content_type__model='exercise_log',
                                                        codename='view_exercise_log')

    perm_view_calorie_goal = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                             content_type__model='calorie_goal',
                                                             codename='view_calorie_goal')

    member_permissions = chain(perm_view_member,
                            	daily_macro_goal_permissions,
                                perm_view_food,
                                meal_food_permissions,
                                meal_log_permissions,
                                exercise_permissions,
                                exercise_log_permissions,
                                calorie_goal_permissions)

    sysadmin_permissions = chain(member_permissions,
                                     daily_macro_goal_permissions,
                                     food_permissions,
                                     meal_food_permissions,
                                     meal_log_permissions,
                                     exercise_permissions,
                                     exercise_log_permissions,
                                     calorie_goal_permissions)



    my_groups_initialization_list = [
        {
            "name": "member",
            "permissions_list": member_permissions,
        },
        {
            "name": "sysadmin",
            "permissions_list": sysadmin_permissions,
        },
        
    ]
    return my_groups_initialization_list


def add_group_permissions_data(apps, schema_editor):
    groups_initialization_list = populate_permissions_lists(apps)

    group_model_class = apps.get_model('auth', 'Group')
    for group in groups_initialization_list:
        if group['permissions_list'] is not None:
            group_object, created = group_model_class.objects.get_or_create(
                name=group['name']
            )
            group_object.permissions.set(group['permissions_list'])
            group_object.save()


def remove_group_permissions_data(apps, schema_editor):
    groups_initialization_list = populate_permissions_lists(apps)

    group_model_class = apps.get_model('auth', 'Group')
    for group in groups_initialization_list:
        if group['permissions_list'] is not None:
            group_object = group_model_class.objects.get(
                name=group['name']
            )
            list_of_permissions = group['permissions_list']
            for permission in list_of_permissions:
                group_object.permissions.remove(permission)
                group_object.save()


class Migration(migrations.Migration):
    dependencies = [
        ('calorie_counter', '0005_calorie_counter_create_groups'),
    ]

    operations = [
        migrations.RunPython(
            add_group_permissions_data,
            remove_group_permissions_data
        )
    ]

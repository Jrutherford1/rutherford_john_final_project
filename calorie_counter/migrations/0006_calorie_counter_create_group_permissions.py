from __future__ import unicode_literals
from itertools import chain

from django.db import migrations


def populate_permissions_lists(apps):
    permission_class = apps.get_model('auth', 'Permission')

    # member_permissions = permission_class.objects.filter(content_type__app_label='calorie_counter',
    #                                                      content_type__model='member')

    dailymacrogoal_permissions = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                                 content_type__model='dailymacrogoal')

    food_permissions = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                       content_type__model='food')

    mealfood_permissions = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                           content_type__model='mealfood')

    meallog_permissions = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                          content_type__model='meallog')

    exercise_permissions = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                           content_type__model='exercise')

    exerciselog_permissions = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                              content_type__model='exerciselog')

    caloriegoal_permissions = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                              content_type__model='caloriegoal')

    perm_view_member = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                       content_type__model='member',
                                                       codename='view_member')

    # perm_view_dailymacrogoal = permission_class.objects.filter(content_type__app_label='calorie_counter',
    #                                                            content_type__model='dailymacrogoal',
    #                                                            codename='view_dailymacrogoal')

    perm_view_food = permission_class.objects.filter(content_type__app_label='calorie_counter',
                                                     content_type__model='food',
                                                     codename='view_food')

    # perm_view_mealfood = permission_class.objects.filter(content_type__app_label='calorie_counter',
    #                                                      content_type__model='mealfood',
    #                                                      codename='view_mealfood')
    #
    # perm_view_meallog = permission_class.objects.filter(content_type__app_label='calorie_counter',
    #                                                     content_type__model='meallog',
    #                                                     codename='view_meallog')
    #
    # perm_view_exercise = permission_class.objects.filter(content_type__app_label='calorie_counter',
    #                                                      content_type__model='exercise',
    #                                                      codename='view_exercise')
    #
    # perm_view_exerciselog = permission_class.objects.filter(content_type__app_label='calorie_counter',
    #                                                         content_type__model='exerciselog',
    #                                                         codename='view_exerciselog')
    #
    # perm_view_caloriegoal = permission_class.objects.filter(content_type__app_label='calorie_counter',
    #                                                         content_type__model='caloriegoal',
    #                                                         codename='view_caloriegoal')

    member_permissions = chain(perm_view_member,
                               dailymacrogoal_permissions,
                               perm_view_food,
                               mealfood_permissions,
                               meallog_permissions,
                               exercise_permissions,
                               exerciselog_permissions,
                               caloriegoal_permissions)

    sysadmin_permissions = chain(member_permissions,
                                 dailymacrogoal_permissions,
                                 food_permissions,
                                 mealfood_permissions,
                                 meallog_permissions,
                                 exercise_permissions,
                                 exerciselog_permissions,
                                 caloriegoal_permissions)

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

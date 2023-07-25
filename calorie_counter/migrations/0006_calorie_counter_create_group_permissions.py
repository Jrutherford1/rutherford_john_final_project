from __future__ import unicode_literals
from itertools import chain

from django.db import migrations


def populate_permissions_lists(apps):
    permission_class = apps.get_model('auth', 'Permission')

    perm_view_member = permission_class.objects.filter(
        content_type__app_label='calorie_counter',
        content_type__model='member',
        codename='view_member'
    )

    perm_view_food = permission_class.objects.filter(
        content_type__app_label='calorie_counter',
        content_type__model='food',
        codename='view_food'
    )

    member_permissions = chain(perm_view_member, perm_view_food)

    sysadmin_permissions = permission_class.objects.filter(
        content_type__app_label='calorie_counter')

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

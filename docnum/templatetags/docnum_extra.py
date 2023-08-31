from django import template
from django.contrib.auth.models import Group
from docnum.views import MNGR_GROUP
from django.utils import timezone

register = template.Library()
mngr_group = Group.objects.get(name=MNGR_GROUP)


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='can_update')
def can_update(user, contra):
    if contra.is_valid:
        if contra.status.name == "已取號":
            if user.id == contra.created_by.id:
                return True
            return False
        elif contra.status.name == "已歸檔":
            if mngr_group in user.groups.all():
                return True
            return False
        else:
            return False
    else:
        return False


@register.filter(name='can_confirm')
def can_confirm(user, contra):
    if contra.is_valid:
        if contra.status.name in ["已取號", "已確認"]:
            if user.id == contra.created_by.id:
                return True
            return False
        else:
            return False
    else:
        return False


@register.filter(name='can_disable')
def can_disable(user, contra):
    if contra.is_valid:
        if mngr_group in user.groups.all():
            return True
        elif user.id is contra.created_by.id:
            if contra.status.name == "已取號":
                return True
            else:
                return False
        else:
            return False
    else:
        print('contract is not valid')
        return False


@register.filter(name='can_archive')
def can_archive(user, contra):
    if contra.status.name != "已歸檔" and mngr_group in user.groups.all():
        return True
    else:
        return False


@register.filter(name='ifexpired')
def ifexpired(end_date):
    return end_date < timezone.localtime().date()
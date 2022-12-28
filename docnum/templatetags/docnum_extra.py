from django import template
from django.contrib.auth.models import Group
from docnum.models import Contract
from docnum.views import MNGR_GROUP

register = template.Library()
mngr_group = Group.objects.get(name=MNGR_GROUP)


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='can_update')
def can_update(user, contra):
    print(user.groups.all())
    if contra.is_valid:
        if contra.status.name == "已取號":
            if user.id == contra.created_by.id:
                return True
            return False
        else:
            if mngr_group in user.groups.all():
                return True
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
        if user.id is contra.created_by.id:
            if contra.status.name == "已取號":
                return True
        elif MNGR_GROUP in user.groups.all():
            return True
        else:
            return False
    else:
        print('contract is not valid')
        return False

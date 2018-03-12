from django.contrib.admin import register
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


class WebadminSite(AdminSite):
    pass


site = WebadminSite()


@register(get_user_model(), site=site)
class UserAdmin(UserAdmin):
    pass

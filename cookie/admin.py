from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User


class CookieTrailsAdminSite(admin.AdminSite):
    site_header = "Cookie Trails Admin"
    site_title = "Cookie Trails Admin"
    index_title = "Cookie Trails Admin"
    enable_nav_sidebar = False


admin_site = CookieTrailsAdminSite()
admin_site.register(Group, GroupAdmin)
admin_site.register(User, UserAdmin)

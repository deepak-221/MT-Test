from django.contrib import admin
from .models import User, StudentClass
from django.contrib.auth.models import Group

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'date_of_birth', 'is_active', 'image', 'student_class']

    def get_queryset(self, request):
        queryset = super(UserAdmin, self).get_queryset(request)
        return queryset.exclude(is_superuser=True)

    def get_form(self, request, obj=None, **kwargs):
        exclude_data = ['is_superuser', 'groups', 'user_permissions', 'password', 'last_login', 'is_staff',
                        'date_joined']
        self.exclude = exclude_data
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        for field in form.base_fields:
            if form.base_fields.get(field).required:
                form.base_fields.get(field).label_suffix = " *:"
        form.request = request
        return form

    def name(self, obj):
        return '%s %s' % (obj.first_name, obj.last_name)


admin.site.register(User, UserAdmin)
admin.site.register(StudentClass)
admin.site.unregister(Group)

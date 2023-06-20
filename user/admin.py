from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from .models import User, Student, StudentProfile

# Register your models here.

class StudentProfileInLine(admin.StackedInline):
    model = StudentProfile
    can_delete = False

class AccountsStudentAdmin(AuthUserAdmin):
    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(AccountsStudentAdmin, self).add_view(*args, **kwargs)
    def change_view(self, *args, **kwargs):
        self.inlines = [StudentProfileInLine]
        return super(AccountsStudentAdmin,self).change_view(*args, **kwargs)

admin.site.register(Student, AccountsStudentAdmin)
admin.site.register(StudentProfile)
admin.site.register(User)
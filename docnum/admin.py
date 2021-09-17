from django.contrib import admin
from .models import Company, Department, OfficalDoc

# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'valid')


class DeptAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'valid')


class OffDocAdmin(admin.ModelAdmin):
    list_display = ('id', 'pubdate', 'comp', 'dept', 'author', 'fullsn')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Department, DeptAdmin)
admin.site.register(OfficalDoc, OffDocAdmin)

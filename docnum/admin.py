from django.contrib import admin
from .models import Company, Department, OfficalDoc, ReceiveDoc

# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'valid')


class DeptAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'valid')


class OffDocAdmin(admin.ModelAdmin):
    list_display = ('id', 'pubdate', 'comp', 'dept', 'author', 'fullsn')


class RcvDocAdmin(admin.ModelAdmin):
    list_display = ('id', 'addtime', 'senddept', 'author', 'fullsn')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Department, DeptAdmin)
admin.site.register(OfficalDoc, OffDocAdmin)
admin.site.register(ReceiveDoc, RcvDocAdmin)

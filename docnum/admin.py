from django.contrib import admin
from .models import Company, Department, OfficalDoc, ReceiveDoc, ContractCate, ContractStatus, ContractTaxStatus\
    , Project, Contract, ContactLoan, GroupDeptRelation
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'plmsn', 'fullname', 'valid')


class DeptAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'valid')


class OffDocAdmin(admin.ModelAdmin):
    list_display = ('id', 'pubdate', 'comp', 'dept', 'author', 'fullsn')


class RcvDocAdmin(admin.ModelAdmin):
    list_display = ('id', 'addtime', 'senddept', 'author', 'fullsn')


class ContractCateAdmin(SimpleHistoryAdmin):
    list_display = ('sn', 'name', 'is_valid')


class ContractStatusAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'is_valid')


class ContractTaxStatusAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'is_valid')


class ProjectAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'order', 'is_valid')


class ContractAdmin(SimpleHistoryAdmin):
    list_display = ('sn', 'status', 'comp', 'category', 'counterparty', 'changed_by', 'update_time', 'add_time')


class ContractLoanAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'sn', 'contra', 'created_by', 'out_time', 'in_time', 'add_time')


class GroupDeptRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'dept')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Department, DeptAdmin)
admin.site.register(OfficalDoc, OffDocAdmin)
admin.site.register(ReceiveDoc, RcvDocAdmin)
admin.site.register(ContractCate, ContractCateAdmin)
admin.site.register(ContractStatus, ContractStatusAdmin)
admin.site.register(ContractTaxStatus, ContractTaxStatusAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(ContactLoan, ContractLoanAdmin)
admin.site.register(GroupDeptRelation, GroupDeptRelationAdmin)

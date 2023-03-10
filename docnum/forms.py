from django import forms
from django.contrib.auth.models import User
from .models import OfficalDoc, ReceiveDoc, Company, Department, Contract

User.__str__ = lambda user_instance: "{}{}".format(user_instance.last_name, user_instance.first_name)

USER_CHOICE = ()
for ltnm, fstnm in User.objects.all().values_list('last_name', 'first_name'):
    USER_CHOICE += ((ltnm + fstnm, ltnm + fstnm),)

DEPT_CHOICES = ()
for fullname in Department.objects.filter(valid=True):
    DEPT_CHOICES += ((fullname, fullname),)


class AddDocForm(forms.ModelForm):

    class Meta:
        model = OfficalDoc
        fields = "__all__"
        widgets = {
            'comp': forms.Select(attrs={'class': 'custom-select'}),
            'dept': forms.Select(attrs={'class': 'custom-select'}),
            'author': forms.Select(attrs={'class': 'custom-select'}),
            'sn': forms.TextInput(attrs={'class': 'form-control-plaintext'}),
            'fullsn': forms.TextInput(attrs={'class': 'form-control-plaintext'}),
            'pubdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'title': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AddReceiveDocForm(forms.ModelForm):

    class Meta:
        model = ReceiveDoc
        exclude = ['addtime']
        widgets = {
            'sn': forms.TextInput(attrs={'class': 'form-control-plaintext'}),
            'fullsn': forms.TextInput(attrs={'class': 'form-control-plaintext'}),
            'senddept': forms.TextInput(attrs={'class': 'form-control'}),
            'sendsn': forms.TextInput(attrs={'class': 'form-control'}),
            'senddate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rcvcomp': forms.Select(attrs={'class': 'custom-select'}),
            'author': forms.Select(attrs={'class': 'custom-select'}),
        }


class AddCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['fullname', 'shortname']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'shortname': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 2}),
        }


class AddDepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ['fullname', 'shortname']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'shortname': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddContractForm(forms.ModelForm):

    counter_dept = forms.ChoiceField(label="承辦單位*", widget=forms.Select(attrs={'class': 'custom-select'}), choices=DEPT_CHOICES)
    counter_contact = forms.ChoiceField(label="承辦人*", widget=forms.Select(attrs={'class': 'custom-select'}), choices=USER_CHOICE)

    class Meta:
        model = Contract
        exclude = ['add_time', 'update_time', 'is_valid']
        labels = {
            'comp': '公司名稱*',
            'category': '合約類型*',
            'sign_date': '訂約日期',
            'length': '合約年限',
            'start_date': '合約起日',
            'end_date': '合約迄日',
            'counterparty': '合約對象*',
            'counter_dept': '承辦單位*',
            'counter_contact': '承辦人*',
            'total_price': '合約總價*',
            'tax_status': '印花稅*',
            'tax': '印花稅金額',
            'payment': '付款條件',
            'content': '合約主要內容*',
            'manage_dept': '管理部門',
            'manager': '管理人',
            'location': '合約存放處(櫃號)',
            'project': '專案名稱',
            'remark': '備註',
        }
        widgets = {
            'comp': forms.Select(attrs={'class': 'custom-select'}),
            'category': forms.Select(attrs={'class': 'custom-select'}),
            'sign_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'length': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'counterparty': forms.TextInput(attrs={'class': 'form-control'}),
            'counter_dept': forms.TextInput(attrs={'class': 'form-control'}),
            'counter_contact': forms.Select(attrs={'class': 'custom-select'}),
            'total_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'tax_status': forms.Select(attrs={'class': 'custom-select'}),
            'tax': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'payment': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '(請簡短描述合約主旨，例:承租枋寮鄉內寮村段631地號。)',
            }),
            'manage_dept': forms.Select(attrs={'class': 'custom-select'}),
            'manager': forms.Select(attrs={'class': 'custom-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'custom-select'}),
            'remark': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '(補充記載其他事項，例:作為太陽光電案場通行、埋設管線與物料暫置之用。)',
            }),
        }


class UpdateContractForm(forms.ModelForm):

    counter_dept = forms.ChoiceField(label="承辦單位*", widget=forms.Select(attrs={'class': 'custom-select'}), choices=DEPT_CHOICES)
    counter_contact = forms.ChoiceField(label="承辦人*", widget=forms.Select(attrs={'class': 'custom-select'}), choices=USER_CHOICE)


    class Meta:
        model = Contract
        exclude = ['sn', 'comp', 'category', 'add_time', 'update_time', 'is_valid', 'status', 'created_by']
        labels = {
            'sign_date': '訂約日期',
            'length': '合約年限',
            'start_date': '合約起日',
            'end_date': '合約迄日',
            'counterparty': '合約對象*',
            'counter_dept': '承辦單位*',
            'counter_contact': '承辦人*',
            'total_price': '合約總價*',
            'tax_status': '印花稅*',
            'tax': '印花稅金額',
            'payment': '付款條件',
            'content': '合約主要內容*',
            'manage_dept': '管理部門',
            'manager': '管理人',
            'location': '合約存放處(櫃號)',
            'project': '專案名稱',
            'remark': '備註',
        }
        widgets = {
            'sign_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'length': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'counterparty': forms.TextInput(attrs={'class': 'form-control'}),
            'counter_dept': forms.TextInput(attrs={'class': 'form-control'}),
            'counter_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'total_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'tax_status': forms.Select(attrs={'class': 'custom-select'}),
            'tax': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'payment': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'manage_dept': forms.Select(attrs={'class': 'custom-select'}),
            'manager': forms.Select(attrs={'class': 'custom-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'custom-select'}),
            'remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

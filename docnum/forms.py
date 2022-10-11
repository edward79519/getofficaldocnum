from django import forms
from .models import OfficalDoc, ReceiveDoc, Company, Department


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

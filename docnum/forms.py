from django import forms
from .models import OfficalDoc


class AddDocForm(forms.ModelForm):

    class Meta:
        model = OfficalDoc
        fields = "__all__"
        widgets = {
            'comp': forms.Select(attrs={'class': 'custom-select'}),
            'dept': forms.Select(attrs={'class': 'custom-select'}),
            'author': forms.Select(attrs={'class': 'custom-select'}),
            'sn': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'fullsn': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'pubdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'title': forms.Textarea(attrs={'class': 'form-control'}),
        }
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label="帳號:",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError('密码长度不能小于6位')
        return password


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)
    invite_code = forms.CharField(required=False)
    mail_code = forms.CharField(required=False)

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('密码不一致')
        return self.cleaned_data

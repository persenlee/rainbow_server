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
    need_confirm = True
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=False)
    invite_code = forms.CharField(required=False)
    mail_code = forms.CharField(required=False)

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if self.need_confirm and password != confirm_password:
            raise forms.ValidationError('密码不一致')
        return self.cleaned_data


class ProfileForm(forms.Form):
    id = forms.IntegerField(required=True)
    name = forms.CharField(required=False)
    avatar = forms.CharField(required=False)
    age = forms.IntegerField(required=False)
    gender = forms.IntegerField(required=False)
    mobile = forms.CharField(required=False)
    active = forms.BooleanField(required=False)
    invite = forms.BooleanField(required=False)

    def clean(self):
        age = self.cleaned_data.get('age', None)
        if age is not None:
            if age < 0 or age > 150:
                raise forms.ValidationError('👽 forbidden')
        return self.cleaned_data


class MailForm(forms.Form):
    email = forms.EmailField(required=True)

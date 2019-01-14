import django.forms


class ReportForm(forms.Form):
    image_id = forms.CharField(required=True)
    reports = forms.CharField(required=True)

    def clean(self):
        return self.cleaned_data
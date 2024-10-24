from .models import ContactUs
from django import forms


class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = ("name", "email", "query")

        widgets = {
            "query": forms.Textarea(attrs={"rows": 5, "cols": 10}),
        }

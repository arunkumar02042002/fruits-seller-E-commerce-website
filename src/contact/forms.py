from django import forms

from contact.models import ContactUs

from users.dbio import UserDBIO

class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = ("name", "email", "query")

        widgets = {
            "query": forms.Textarea(attrs={"rows": 5, "cols": 10}),
        }

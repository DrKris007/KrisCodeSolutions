from django import forms

from .models import ContactInquiry


class ContactForm(forms.ModelForm):
    # Honeypot: real visitors never see or fill this field.
    website = forms.CharField(
        required=False,
        label="Leave this field empty",
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
    )

    class Meta:
        model = ContactInquiry
        fields = ["full_name", "email", "subject", "message"]
        labels = {
            "full_name": "Full Name",
            "email": "Email Address",
            "subject": "Subject",
            "message": "Project Details / Message",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your full name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com", "autocomplete": "email"}),
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "What is this about?"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 6, "placeholder": "Tell us about your business and what you would like to build."}),
        }

    def clean_full_name(self):
        value = self.cleaned_data["full_name"].strip()
        if len(value) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return value

    def clean_subject(self):
        value = self.cleaned_data["subject"].strip()
        if len(value) < 3:
            raise forms.ValidationError("Please enter a short subject (at least 3 characters).")
        return value

    def clean_message(self):
        value = self.cleaned_data["message"].strip()
        if len(value) < 20:
            raise forms.ValidationError("Please give us a little more detail (at least 20 characters).")
        return value

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return ""

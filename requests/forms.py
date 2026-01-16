from django import forms

from core.forms import BootstrapFormMixin

from .models import HireRequest


class HireRequestForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = HireRequest
        fields = ["subject", "message", "budget", "timeline", "attachment"]

    def clean_budget(self):
        budget = self.cleaned_data.get("budget")
        if budget is not None and budget < 0:
            raise forms.ValidationError("Budget must be a positive value.")
        return budget


class HireRequestStatusForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = HireRequest
        fields = ["status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].choices = [
            (HireRequest.Status.ACCEPTED, "Accepted"),
            (HireRequest.Status.REJECTED, "Rejected"),
        ]

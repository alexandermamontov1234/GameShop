from django import forms
from .models import Review


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body', 'rate')


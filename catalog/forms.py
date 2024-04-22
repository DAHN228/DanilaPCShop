# forms.py
from django import forms
from .models import Review

class ReviewForm(forms.Form):
    review_text = forms.CharField(widget=forms.Textarea)
    product_id = forms.IntegerField(widget=forms.HiddenInput)

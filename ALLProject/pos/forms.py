from django import forms
from .models import Product

class ItemCodeForm(forms.Form):
    item_code = forms.IntegerField(widget=forms.NumberInput(
                                    attrs={'id': 'itemCode'}))

class QuantityForm(forms.Form):
    item_quantity = forms.IntegerField(min_value=1, label="Quantity :",
                                  widget=forms.NumberInput(
                                      attrs={'id': 'quantity'}))
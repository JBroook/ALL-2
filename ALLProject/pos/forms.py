from django import forms

class ItemCodeForm(forms.Form):
    item_code = forms.IntegerField(widget=forms.NumberInput(
                                    attrs={'id': 'itemCode'}))

class QuantityForm(forms.Form):
    item_quantity = forms.IntegerField(min_value=1, label="Quantity :",
                                  widget=forms.NumberInput(
                                      attrs={'id': 'quantity'}))

class CheckOutForm(forms.Form):
    check_out = forms.CharField(required=False, widget=forms.HiddenInput(
                                attrs={'id':'cartForm', 'value':'true'}))
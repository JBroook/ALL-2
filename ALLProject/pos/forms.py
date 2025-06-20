from django import forms

class ItemCodeForm(forms.Form):
    item_code = forms.IntegerField(widget=forms.NumberInput(
                                    attrs={'id': 'itemCode'}))

class QuantityForm(forms.Form):
    item_quantity = forms.IntegerField(min_value=1, label="Quantity :",
                                  widget=forms.NumberInput(
                                      attrs={'id': 'quantity-input'}))

class CheckOutForm(forms.Form):
    check_out = forms.CharField(required=False, widget=forms.HiddenInput(
                                attrs={'id':'cartForm', 'value':'true'}))
    
    payment_method = forms.ChoiceField(required=True,
                                        choices=[('cash', 'Cash'), ('debit_card', 'Debit/Credit Card')],
                                        widget=forms.HiddenInput(attrs={'id':'paymentMethod'}))
    
    cashPaid = forms.FloatField(required=False,
                                widget=forms.TextInput(attrs={'id':'cash-paid'}))
    
    card_number = forms.CharField(required=False, max_length=16,
                                  widget=forms.TextInput(attrs={'class':'card-info', 'id':'cardNo', 'placeholder':'Card Number'}))
    
    expiry = forms.CharField(required=False, max_length=5,
                             widget=forms.TextInput(attrs={'class':'card-info sec expiry', 'id':'cardExp', 'placeholder':'MM/YY'}))
    
    cvv = forms.CharField(required=False, max_length=4,
                          widget=forms.TextInput(attrs={'class':'card-info sec cvv', 'id':'cardCVV', 'placeholder':'Security Num'}))
    
class ClearCartItems(forms.Form):
    clear_cart = forms.BooleanField(required=False, 
                                    widget=forms.HiddenInput(attrs={'id':'clear_cart','value':'True'}))
    
class ClearLastCartItem(forms.Form):
    clear_last = forms.BooleanField(required=False,
                                    widget=forms.HiddenInput(attrs={'id':'clear_last','value':'True'}))
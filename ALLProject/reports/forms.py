from django import forms

class printSales(forms.Form):
    sales_report = forms.BooleanField(required=False, 
                                    widget=forms.HiddenInput(attrs={'id':'sales_report','value':'True'}))
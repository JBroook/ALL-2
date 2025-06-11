from django import forms

class printSales(forms.Form):
    sales_report = forms.BooleanField(required=False, 
                                    widget=forms.HiddenInput(attrs={'id':'sales_report','value':'True'}))
    month_or_day = forms.ChoiceField(required=False,
                                     choices=[('day','Day'),('month','Month')],
                                     widget=forms.HiddenInput(attrs={'id':'monthday'}))
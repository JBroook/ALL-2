from django import forms
from .models import Product, Category, Restock

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['qr_code']
        labels = {
            'name' : "Name",
            'category' : "Category",
            'price' : 'Price',
            'quantity' : 'Quantity',
            'supplier' : 'Supplier',
            'image' : 'Image',
            'alert_threshold' : 'Alert Notice'
        }

        category = forms.ModelChoiceField(queryset=Category.objects.all()),

        widgets = {
            'name' : forms.TextInput(
                attrs={
                    'placeholder':'e.g. Milk', 'class':'form-control'
                    }),
            'price' : forms.NumberInput(attrs={
                'placeholder':'e.g. 5.99', 'class':'form-control'}),
            'quantity' : forms.NumberInput(attrs={
                'placeholder':'e.g. 100', 'class':'form-control'}),
            'supplier' : forms.TextInput(attrs={
                'placeholder':'e.g. Milk & Lawson', 'class':'form-control'}),
            'image' : forms.FileInput(attrs={
                'class':'form-control'}),
            'alert_threshold' : forms.NumberInput(attrs={
                'placeholder':'e.g. 5', 'class':'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

class DateInput(forms.DateInput):
    input_type = 'date'

class RestockForm(forms.ModelForm):
    product_id = -1

    class Meta:
        model = Restock
        fields = '__all__'
        exclude = ['product']
        labels = {
            'cpu' : "Cost Per Unit",
            'units' : "Unit(s) in Batch",
            'date' : "Date Stocked"
        }

        category = forms.ModelChoiceField(queryset=Category.objects.all()),

        widgets = {
            'date' : DateInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.product_id = kwargs.get('product_id')

from django import forms

from conf.utils import bootstrapify
from product.models import *
from os.path import splitext

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name']


class ProductUnitForm(forms.ModelForm):
    class Meta:
        model = ProductUnit
        fields = ['name', 'code']
        
        
class ProductVariationForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        fields = ['name', 'unit']


class ProductVariationPriceForm(forms.ModelForm):
    class Meta:
        model = ProductVariationPrice
        fields = ['product', 'unit', 'price']
        
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ['create_date', 'update_date']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['create_date', 'update_date']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(ItemForm, self).__init__(*args, **kwargs)
        if hasattr(request.user, 'supplier_admin'):
            self.fields['supplier'].widget = forms.HiddenInput()
            self.fields['supplier'].initial = 1

    def clean(self):
        supplier_price = self.cleaned_data.get('supplier_price')
        price = self.cleaned_data.get('price')
        if supplier_price > price:
            raise forms.ValidationError('Supplier price cannot be higher than the retail price')


class SupplierUserForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput)
    password = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput)
    msisdn = forms.CharField(max_length=150)

    def __init__(self, *args, **kwargs):
        # instance = kwargs.pop("instance", None)
        super(SupplierUserForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields.pop('password')
            self.fields.pop('confirm_password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'msisdn', 'is_active', 'username', 'password',
                  'confirm_password']


class SalesCommissionForm(forms.ModelForm):
    class Meta:
        model = SalesCommission
        exclude = ['create_date', 'update_date']


class ItemAdditionChargesForm(forms.ModelForm):
    class Meta:
        model = ItemAdditionalCharges
        exclude = ['create_date', 'update_date']


class ItemCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        exclude = ['create_date', 'update_date']


class ItemUploadForm(forms.Form):
    sheetChoice = (
        ('1', 'sheet1'),
        ('2', 'sheet2'),
        ('3', 'sheet3'),
        ('4', 'sheet4'),
        ('5', 'sheet5'),
        ('6', 'sheet6'),
        ('7', 'sheet7'),
        ('8', 'sheet8'),
        ('9', 'sheet9'),
        ('10', 'sheet10'),
    )

    rowchoices = (
        ('1', 'Row 1'),
        ('2', 'Row 2'),
        ('3', 'Row 3'),
        ('4', 'Row 4'),
        ('5', 'Row 5')
    )

    choices = list()
    for i in range(65, 91):
        choices.append([i - 65, chr(i)])

    excel_file = forms.FileField()
    sheet = forms.ChoiceField(label="Sheet", choices=sheetChoice, widget=forms.Select(attrs={'class': 'form-control'}))
    row = forms.ChoiceField(label="Row", choices=rowchoices, widget=forms.Select(attrs={'class': 'form-control'}))
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all())
    item_col = forms.ChoiceField(label='Item Column', initial=0, choices=choices,
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        help_text='The column containing the Farmers Name')
    supplier_price_col = forms.ChoiceField(label='Supplier Price Column', initial=1, choices=choices,
                               widget=forms.Select(attrs={'class': 'form-control'}),
                               help_text='The column containing the Gender')
    retail_price_col = forms.ChoiceField(label='Retail Price Column', initial=2, choices=choices,
                                widget=forms.Select(attrs={'class': 'form-control'}),
                                help_text='The column containing the NIN')

    category_column = forms.ChoiceField(label='Category', initial=3, choices=choices,
                                          widget=forms.Select(attrs={'class': 'form-control'}),
                                          help_text='The column containing the Date of birth. Format YYYY-MM-DD')


    def clean(self):
        data = self.cleaned_data
        f = data.get('excel_file', None)
        ext = splitext(f.name)[1][1:].lower()
        if not ext in ["xlsx", "xls"]:
            raise forms.ValidationError(("The File type is not accepted"))
        return data


bootstrapify(ItemUploadForm)
bootstrapify(SupplierForm)
bootstrapify(ItemForm)
bootstrapify(ItemCategoryForm)
bootstrapify(ItemAdditionChargesForm)
bootstrapify(ProductForm)
bootstrapify(ProductUnitForm)
bootstrapify(ProductVariationForm)
bootstrapify(ProductVariationPriceForm)
bootstrapify(SupplierUserForm)
bootstrapify(SalesCommissionForm)

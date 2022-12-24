from django import forms
from partner.models import *
from conf.models import District
from conf.utils import bootstrapify
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class PartnerForm(forms.ModelForm):
    
    class Meta:
        model = Partner
        fields = ['name', 'code', 'logo', 'system_url', 'system_theme', 'phone_number', 'email', 'address', 'is_active']


class PartnerStaffForm(UserCreationForm):
    role = models.CharField(max_length=120, choices=(('Excecutive','Excecutive'), ('Business Development','Business Development'), ('Officer', 'Officer')))
    phone_number = forms.CharField(max_length=255)
    district = forms.ModelMultipleChoiceField(queryset=District.objects.all(), widget=forms.SelectMultiple)


    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + (
        "first_name", "last_name", "email", "is_active", "phone_number", "district")

    def __init__(self, *args, **kwargs):
        super(PartnerStaffForm, self).__init__(*args, **kwargs)
        self.fields['district'].widget.attrs.update({'class': "selec_adv_1"})


class PartnerStaffChangeForm(UserChangeForm):
    role = models.CharField(max_length=120, choices=(('Excecutive','Excecutive'), ('Business Development','Business Development'), ('Officer', 'Officer')))
    phone_number = forms.CharField(max_length=255)
    district = forms.ModelMultipleChoiceField(queryset=District.objects.all(), widget=forms.SelectMultiple)

    class Meta(UserChangeForm.Meta):
        exclude = ['groups', 'user_permissions', 'is_staff', 'is_superuser', 'date_joined', 'last_login']

    def __init__(self, *args, **kwargs):
        super(PartnerStaffChangeForm, self).__init__(*args, **kwargs)
        self.fields['district'].widget.attrs.update({'class': "selec_adv_1"})



class PartnerStaffForm_deprecated(forms.ModelForm):
    username = forms.CharField(max_length=150, required=False)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(max_length=150, widget=forms.PasswordInput(), required=False)
    
    class Meta:
        model = PartnerStaff
        exclude = ['create_date', 'update_date']
    
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop("instance", None)
        super(PartnerStaffForm, self).__init__(instance=instance, *args, **kwargs)
        self.fields['district'].widget.attrs.update({'class': "selec_adv_1"})

bootstrapify(PartnerForm)
bootstrapify(PartnerStaffForm)
bootstrapify(PartnerStaffChangeForm)
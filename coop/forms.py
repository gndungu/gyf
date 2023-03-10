import xlrd
from django.utils import timezone
from django import forms
from os.path import splitext
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms.formsets import formset_factory, BaseFormSet

from conf.utils import bootstrapify, internationalize_number, PHONE_REGEX
from coop.models import *
from conf.models import District, SubCounty, Village, Parish, PaymentMethod
from product.models import ProductVariation
from userprofile.models import Profile
from django.contrib.auth.models import User


class CooperativeForm(forms.ModelForm):
    class Meta:
        model = Cooperative
        fields = ['name', 'logo', 'district', 'county', 'sub_county', 'parish', 'village', 'phone_number', 'address', 'contact_person_name',
                  'product', 'is_active', 'send_message', 'sms_api_url', 'sms_api_token', 'payments_account',
                  'payments_token', 'payments_authentication', 'system_url', 'coop_abbreviation']
    
    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            try:
                phone_number = internationalize_number(phone_number)
                self.cleaned_data['phone_number'] = phone_number
            except ValueError:
                raise forms.ValidationError("Please enter a valid phone number.'%s' is not valid" % phone_number)
        return self.cleaned_data
        

class CooperativeUploadForm(forms.Form):
    
    sheetChoice = (
        ('1','sheet1'),
        ('2','sheet2'),
        ('3','sheet3'),
        ('4','sheet4'),
        ('5','sheet5'),
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
        choices.append([i-65, chr(i)])

    
    excel_file = forms.FileField()
    sheet = forms.ChoiceField(label="Sheet", choices=sheetChoice, widget=forms.Select(attrs={'class':'form-control'}))
    row = forms.ChoiceField(label="Row", choices=rowchoices, widget=forms.Select(attrs={'class':'form-control'}))
    cooperative_col = forms.ChoiceField(label='Cooperative Column', initial=0, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Cooperative')
    district_col = forms.ChoiceField(label='District Column', initial=1, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the District')
    sub_county_col = forms.ChoiceField(label='Sub County Column', initial=2, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Sub County')
    contact_person = forms.ChoiceField(label='Contact Person Column', initial=3, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text="The column contains the Name of the Contact Person")
    phone_number = forms.ChoiceField(label='Phone Number Column', initial=4, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text="The column contains the Phone Number of Cooperative")
    
    
    def clean(self):
        data = self.cleaned_data
        f = data.get('excel_file', None)
        ext = splitext(f.name)[1][1:].lower()
        if not ext in ["xlsx", "xls"]:
            raise forms.ValidationError(("the File type is not accepted"))
        return data
            

class CooperativeSharePriceForm(forms.ModelForm):
    class Meta:
        model = CooperativeSharePrice
        exclude = ['created_by', 'create_date', 'update_date']
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CooperativeSharePriceForm, self).__init__(*args, **kwargs)
        if not self.request.user.profile.is_union():
            self.fields['cooperative'].widget=forms.HiddenInput()
            self.fields['cooperative'].initial=self.request.user.cooperative_admin.cooperative


class FarmerGroupForm(forms.ModelForm):
    class Meta:
        model = FarmerGroup
        exclude = ['create_date', 'update_date', 'cooperative', 'created_by', 'code', 'contribution_total', 'shares']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FarmerGroupForm, self).__init__(*args, **kwargs)
        if not self.request.user.profile.is_union():
            if hasattr(self.request.user, 'partner_admin'):
                self.fields['partner'].widget = forms.HiddenInput()
                self.fields['partner'].initial = self.request.user.partner_admin.partner


class FarmerGroupUploadForm(forms.Form):
    sheetChoice = (
        ('1', 'sheet1'),
        ('2', 'sheet2'),
        ('3', 'sheet3'),
        ('4', 'sheet4'),
        ('5', 'sheet5'),
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

    partner = forms.ModelChoiceField(queryset=Partner.objects.all())
    excel_file = forms.FileField()
    sheet = forms.ChoiceField(label="Sheet", choices=sheetChoice, widget=forms.Select(attrs={'class': 'form-control'}))
    row = forms.ChoiceField(label="Row", choices=rowchoices, widget=forms.Select(attrs={'class': 'form-control'}))
    cooperative_col = forms.ChoiceField(label='Farmer Group Column', initial=0, choices=choices,
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        help_text='The column containing the Names')
    district_col = forms.ChoiceField(label='District Column', initial=1, choices=choices,
                                     widget=forms.Select(attrs={'class': 'form-control'}),
                                     help_text='The column containing the District')
    # county_col = forms.ChoiceField(label=' County Column', initial=2, choices=choices,
    #                                    widget=forms.Select(attrs={'class': 'form-control'}),
    #                                    help_text='The column containing the County')
    sub_county_col = forms.ChoiceField(label='Sub County Column', initial=2, choices=choices,
                                       widget=forms.Select(attrs={'class': 'form-control'}),
                                       help_text='The column containing the Sub County')
    parish_col = forms.ChoiceField(label='Parish Column', initial=3, choices=choices,
                                       widget=forms.Select(attrs={'class': 'form-control'}),
                                       help_text='The column containing the Parish')
    village_col = forms.ChoiceField(label='Village Column', initial=4, choices=choices,
                                   widget=forms.Select(attrs={'class': 'form-control'}),
                                   help_text='The column containing the Village')
    contact_person = forms.ChoiceField(label='Contact Person Column', initial=5, choices=choices,
                                       widget=forms.Select(attrs={'class': 'form-control'}),
                                       help_text="The column contains the Name of the Contact Person")
    phone_number = forms.ChoiceField(label='Phone Number Column', initial=6, choices=choices,
                                     widget=forms.Select(attrs={'class': 'form-control'}),
                                     help_text="The column contains the Phone Number of Cooperative")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FarmerGroupUploadForm, self).__init__(*args, **kwargs)
        if not self.request.user.profile.is_union():
            if hasattr(self.request.user, 'partner_admin'):
                self.fields['partner'].widget=forms.HiddenInput()
                self.fields['partner'].initial=self.request.user.partner_admin.partner

    def clean(self):
        data = self.cleaned_data
        f = data.get('excel_file', None)
        ext = splitext(f.name)[1][1:].lower()
        if not ext in ["xlsx", "xls"]:
            raise forms.ValidationError(("the File type is not accepted"))
        return data


class MemberProfileForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MemberProfileForm, self).__init__(*args, **kwargs)
        
        self.fields['parish'].queryset = Parish.objects.none()
        
        if 'sub_county' in self.data:
            try:
                sub_county_id = int(self.data.get('sub_county'))
                self.fields['parish'].queryset = Parish.objects.filter(sub_county=sub_county_id).order_by('name')
            except Exception as e: #(ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            if self.instance.sub_county:
                self.fields['parish'].queryset = self.instance.sub_county.parish_set.order_by('name')
            
        if not self.request.user.profile.is_union():
            if hasattr(self.request.user, 'cooperative_admin'):
                self.fields['cooperative'].widget=forms.HiddenInput()

                self.fields['cooperative'].initial=self.request.user.cooperative_admin.cooperative
            
    class Meta:
        model = CooperativeMember
        exclude = ['created_by', 'create_date', 'update_date', 'member_id']
    
    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        other_phone_number = self.cleaned_data.get('other_phone_number')
        
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            if date_of_birth > timezone.now().date():
                raise forms.ValidationError("Error! Date of Birth cannot be in the Future")
        
        if phone_number:
            try:
                phone_number = internationalize_number(phone_number)
                self.cleaned_data['phone_number'] = phone_number
            except ValueError:
                raise forms.ValidationError("Please enter a valid phone number.'%s' is not valid" % phone_number)
        if other_phone_number:
            try:
                other_phone_number = internationalize_number(other_phone_number)
                self.cleaned_data['other_phone_number'] = other_phone_number
            except ValueError:
                raise forms.ValidationError("Please enter a valid phone number.'%s' is not valid" % other_phone_number)
        return self.cleaned_data


class MemberProfileSearchForm(forms.Form):
    choices=(('', 'Role'), ('Chairman', 'Chairman'), ('Vice Chairman', 'Vice Chairman'), ('Treasurer', 'Treasurer'),
        ('Secretary', 'Secretary'), ('Member', 'Member'),('Secretary Manager', 'Secretary Manager'), ('Patron', 'Patron'))
        
    name = forms.CharField(max_length=150, required=False)
    start_date = forms.CharField(max_length=150, required=False,
                                 widget=forms.TextInput(attrs={'class': 'some_class', 'id': 'uk_dp_1',
                                                               'data-uk-datepicker': "{format:'YYYY-MM-DD'}",
                                                               'autocomplete': "off"}))
    end_date = forms.CharField(max_length=150, required=False,
                               widget=forms.TextInput(attrs={'class': 'some_class', 'id': 'uk_dp_1',
                                                             'data-uk-datepicker': "{format:'YYYY-MM-DD'}",
                                                             'autocomplete': "off"}))

    phone_number = forms.CharField(max_length=150, required=False)
    farmer_group = forms.ChoiceField(widget=forms.Select(), choices=[], required=False)
    role = forms.ChoiceField(widget=forms.Select(), choices=choices, required=False)
    district = forms.ChoiceField(widget=forms.Select(), choices=[], required=False)
    create_by = forms.ModelChoiceField(queryset=None, required=False)

    def __init__(self,  *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super (MemberProfileSearchForm, self).__init__(*args, **kwargs)
       
        qs = CooperativeMember.objects.values('farmer_group__id', 'farmer_group__name').distinct()
        d_qs = CooperativeMember.objects.values('district__id', 'district__name').distinct()
        choices = [['', 'Farmer Group']]
        dchoices = [['', 'District']]
        for q in qs:
            choices.append([q['farmer_group__id'], q['farmer_group__name']])
        
        for dq in d_qs:
            dchoices.append([dq['district__id'], dq['district__name']])

        self.fields['create_by'].queryset = Profile.objects.all()
        self.fields['farmer_group'].choices = choices
        self.fields['district'].choices = dchoices
        if not self.request.user.profile.is_union():
            self.fields.pop('farmer_group')
            self.fields.pop('create_by')


class MemberUploadForm(forms.Form):
    
    sheetChoice = (
        ('1','sheet1'),
        ('2','sheet2'),
        ('3','sheet3'),
        ('4','sheet4'),
        ('5','sheet5'),
        ('6','sheet6'),
        ('7','sheet7'),
        ('8','sheet8'),
        ('9','sheet9'),
        ('10','sheet10'),
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
        choices.append([i-65, chr(i)])
    
    excel_file = forms.FileField()
    sheet = forms.ChoiceField(label="Sheet", choices=sheetChoice, widget=forms.Select(attrs={'class':'form-control'}))
    row = forms.ChoiceField(label="Row", choices=rowchoices, widget=forms.Select(attrs={'class':'form-control'}))
    farmer_name_col = forms.ChoiceField(label='Farmer Name Column', initial=0, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Farmers Name')
    gender = forms.ChoiceField(label='Gender Column', initial=1, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Gender')
    nin_col = forms.ChoiceField(label='National Identification Column', initial=2, choices=choices,
                                widget=forms.Select(attrs={'class': 'form-control'}),
                                help_text='The column containing the NIN')

    date_of_birth_col = forms.ChoiceField(label='Date of Birth Column', initial=3, choices=choices, widget=forms.Select(attrs={'class':'form-control'}),
                                          help_text='The column containing the Date of birth. Format YYYY-MM-DD')
    phone_number_col = forms.ChoiceField(label='Phone Number Column', initial=4, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Phone Number')
    role_col = forms.ChoiceField(label='Role Column', initial=5, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Cooperate Role')
    year_joined_col = forms.ChoiceField(label='Yeah Joined Column', initial=6, choices=choices, widget=forms.Select(attrs={'class':'form-control'}),
                                        help_text='The column containing the Year the Farmer Joined the FG')
    acreage_col = forms.ChoiceField(label='Acreage Column', initial=7, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Acreage')
    cooperative_col = forms.ChoiceField(label='Farmer Group Column', initial=8, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Farmer Group')
    district_col = forms.ChoiceField(label='Distric Column', initial=9, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the District')
    county_col = forms.ChoiceField(label='County Column', initial=10, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the County')
    sub_county_col = forms.ChoiceField(label='Sub County Column', initial=11, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Sub county')
    parish_col = forms.ChoiceField(label='Parish Column', initial=12, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Parish')
    village_col = forms.ChoiceField(label='Village Column', initial=13, choices=choices, widget=forms.Select(attrs={'class':'form-control'}), help_text='The column containing the Village')

    
    def clean(self):
        data = self.cleaned_data
        f = data.get('excel_file', None)
        ext = splitext(f.name)[1][1:].lower()
        if not ext in ["xlsx", "xls"]:
            raise forms.ValidationError(("The File type is not accepted"))
        return data


class DownloadMemberOptionForm(forms.Form):
    profile = forms.BooleanField(initial=True)
    farm = forms.BooleanField(required=False)
    herd = forms.BooleanField(required=False)
    member_supply = forms.BooleanField(required=False)
    

class CooperativeContributionForm(forms.ModelForm):
    class Meta:
        model = CooperativeContribution
        exclude = ['create_date', 'update_date']
        

class CooperativeShareTransactionForm(forms.ModelForm):
       
    class Meta:
        model = CooperativeShareTransaction
        exclude = ['create_date', 'update_date'] 
    

class MemberSubscriptionForm(forms.ModelForm):
    class Meta:
        model = CooperativeMemberSubscriptionLog
        exclude = ['create_date', 'update_date']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Member is Subscribed for the Year provided",
            }
        }
      
        
class MemberSharesForm(forms.ModelForm):
    cooperative = forms.ChoiceField(widget=forms.Select(), choices=[], required=False)
    class Meta:
        model = CooperativeMemberSharesLog
        exclude = ['create_date', 'update_date']
        
        widgets = {
          'shares': forms.TextInput(attrs={'readonly': True}),
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MemberSharesForm, self).__init__(*args, **kwargs)
        
        qs = Cooperative.objects.all()
        
        choices = [['', 'Cooperative']]
        
        for q in qs:
            choices.append([q.id, q.name])
        
        self.fields['cooperative'].choices = choices
        
        self.fields['cooperative_member'].queryset = CooperativeMember.objects.none()
        
        
            
        if 'cooperative' in self.data:
            
            try:
                
                cooperative_id = int(self.data.get('cooperative'))
                self.fields['cooperative_member'].queryset = CooperativeMember.objects.filter(cooperative=cooperative_id).order_by('first_name')
            except Exception as e: #(ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
               
                self.fields['cooperative_member'].queryset = CooperativeMember.objects.none()
                
        elif self.instance.pk:
            
            if self.instance.cooperative:
                self.fields['cooperative_member'].queryset = self.instance.cooperative.member_set.order_by('first_name')
        if not self.request.user.profile.is_union():
            cooperative = self.request.user.cooperative_admin.cooperative
            price = CooperativeSharePrice.objects.filter(
                cooperative=cooperative).order_by('-create_date')
            self.fields['shares_price'].initial=price[0].price if price else ""
            self.fields['cooperative_member'].queryset = self.fields['cooperative_member'].queryset.filter(cooperative=cooperative)


class VariationSupplyRequestFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        breeds = []
        duplicates = False
        
        
        for form in self.forms:
            if form.cleaned_data:
                breed = form.cleaned_data['breed']
                
                # Check that no two links have the same anchor or URL
                if breed:
                    if breed in breeds:
                        duplicates = True
                    breeds.append(breed)
                
                if duplicates:
                    raise forms.ValidationError(
                        'Duplicate Breeds Found',
                        code='duplicate_values'
                    )

     
class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        exclude = ['create_date', 'update_date']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CollectionForm, self).__init__(*args, **kwargs)
        self.fields['collection_date'].widget=forms.TextInput(attrs={"data-uk-datepicker": "{maxDate:10, format:'YYYY-MM-D'}"})

        if not self.request.user.profile.is_union():
            self.fields['cooperative'].widget=forms.HiddenInput()
            if hasattr(self.request.user, 'cooperative_admin'):
                self.fields['cooperative'].initial=self.request.user.cooperative_admin.cooperative
        
    def clean(self):
        data = self.cleaned_data
        member = data.get('member')
        name = data.get('name')
        phone_number = data.get('phone_number')
        if not member:
            if not name and not phone_number:
                raise forms.ValidationError("Error! Please Select a Member or provide the Name of a non-member")
        if phone_number:       
            try:
                phone_number = internationalize_number(phone_number)
                self.cleaned_data['phone_number'] = phone_number
            except ValueError:
                raise forms.ValidationError("Please enter a valid phone number.'%s' is not valid" % phone_number)
        
        return data
    
    
class CollectionFilterForm(forms.Form):
    search = forms.CharField(max_length=160, required=False)
    cooperative = forms.ChoiceField(widget=forms.Select(), choices=[], required=False)
    product = forms.ChoiceField(widget=forms.Select(), required=False)
    start_date = forms.CharField(max_length=160, required=False, widget=forms.TextInput(attrs={"data-uk-datepicker":"{format:'YYYY-MM-DD'}"}))
    end_date = forms.CharField(max_length=160, required=False, widget=forms.TextInput(attrs={"data-uk-datepicker":"{format:'YYYY-MM-DD'}"}))
    
    def __init__(self, *args, **kwargs):
        super(CollectionFilterForm, self).__init__(*args, **kwargs)
        choices = [['', '--------------']]
        choices.extend([[pv.id, pv.name]  for pv in ProductVariation.objects.all()])
        self.fields['product'].choices = choices
        choices = [['', 'Cooperative']]
        qs = Cooperative.objects.all()
        for q in qs:
            choices.append([q.id, q.name])
        self.fields['cooperative'].choices = choices


class MemberOrderForm(forms.ModelForm):
    class Meta:
        model = MemberOrder
        fields = ['farmer_group', 'member', 'request_type', 'order_date']
        # widgets = {
        #     'order_date': forms.TextInput(attrs={'autocomplete': 'off'}),
        # }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MemberOrderForm, self).__init__(*args, **kwargs)
        
        if self.request.user.profile.is_cooperative():
            pass
            # self.fields['cooperative'].widget=forms.HiddenInput()
            # self.fields['farmer_group'].widget=forms.HiddenInput()
            # self.fields['cooperative'].initial=self.request.user.cooperative_admin.cooperative
        
        self.fields['member'].queryset = CooperativeMember.objects.none()

        if 'farmer_group' in self.data:
            try:
                farmer_group_id = int(self.data.get('farmer_group'))
                self.fields['member'].queryset = CooperativeMember.objects.filter(farmer_group__id=farmer_group_id).order_by('first_name')
            except Exception as e: #(ValueError, TypeError):
                print("ERROR")
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            if self.instance.cooperative:
                self.fields['member'].queryset = self.instance.cooperative.member_set.order_by('first_name')
    
        
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ['create_date', 'update_date', 'created_by', 'unit_price']
        widgets = {
          'item': forms.Select(attrs={'onChange': 'refreshInput(this)', 'class': 'id_item'}),
          'quantity': forms.TextInput(attrs={'onkeydown': 'calculatePrice(this)'}),
        }


class AgentSearchForm(forms.Form):
    name = forms.CharField(max_length=150, required=False)
    phone_number = forms.CharField(max_length=150, required=False)
    farmer_group = forms.ChoiceField(widget=forms.Select(), choices=[], required=False)
    start_date = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class':'some_class', 'id':'uk_dp_1',
                                                                                               'data-uk-datepicker': "{format:'YYYY-MM-DD'}",
                                                                                               'autocomplete':"off"}))
    end_date = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class':'some_class', 'id':'uk_dp_1',
                                                                                               'data-uk-datepicker': "{format:'YYYY-MM-DD'}",
                                                                                               'autocomplete':"off"}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AgentSearchForm, self).__init__(*args, **kwargs)

        qs = CooperativeMember.objects.values('farmer_group__id', 'farmer_group__name').distinct()

        choices = [['', 'Farmer Groups']]
        for q in qs:
            choices.append([q['farmer_group__id'], q['farmer_group__name']])

        self.fields['farmer_group'].choices = choices


class AgentForm(forms.ModelForm):
    district = forms.MultipleChoiceField(required=False, choices=[])
    farmer_group = forms.MultipleChoiceField(required=False, choices=[])
    confirm_password = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput)
    password = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput)
    msisdn = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'msisdn', 'is_active', 'username', 'password',
                  'confirm_password']

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop("instance", None)
        super(AgentForm, self).__init__(*args, **kwargs)

        self.fields['farmer_group'].choices = [[x.id, x.name] for x in FarmerGroup.objects.all()]
        self.fields['district'].choices = [[x.id, x.name] for x in District.objects.all()]
        self.fields['farmer_group'].widget.attrs.update({'class': "selec_adv_1"})
        self.fields['district'].widget.attrs.update({'class': "selec_adv_1"})

        if instance:
            self.fields.pop('password')
            self.fields.pop('confirm_password')


class AgentUpdateForm(forms.ModelForm):
    district = forms.MultipleChoiceField(required=False, choices=[])
    farmer_group = forms.MultipleChoiceField(required=False, choices=[])
    msisdn = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'msisdn', 'is_active', 'username']

    def __init__(self, *args, **kwargs):
        super(AgentUpdateForm, self).__init__(*args, **kwargs)
        self.fields['farmer_group'].choices = [[x.id, x.name] for x in FarmerGroup.objects.all()]
        self.fields['district'].choices = [[x.id, x.name] for x in District.objects.all()]
        self.fields['farmer_group'].widget.attrs.update({'class': "selec_adv_1"})
        self.fields['district'].widget.attrs.update({'class': "selec_adv_1"})






class AgentUploadForm(forms.Form):
    sheetChoice = (
        ('1', 'sheet1'),
        ('2', 'sheet2'),
        ('3', 'sheet3'),
        ('4', 'sheet4'),
        ('5', 'sheet5'),
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
    name_col = forms.ChoiceField(label='Name Column', initial=0, choices=choices,
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        help_text='The column containing the Names')
    email_column = forms.ChoiceField(label='Email Column', initial=1, choices=choices,
                                     widget=forms.Select(attrs={'class': 'form-control'}),
                                     help_text='The column containing the email')
    phone_number_col = forms.ChoiceField(label='Phone Number Column', initial=2, choices=choices,
                                       widget=forms.Select(attrs={'class': 'form-control'}),
                                       help_text='The column containing the phone number')
    district_col = forms.ChoiceField(label='Distric Column', initial=3, choices=choices,
                                     widget=forms.Select(attrs={'class': 'form-control'}),
                                     help_text='The column containing the District')
    username_col = forms.ChoiceField(label='Password Column', initial=4, choices=choices,
                                       widget=forms.Select(attrs={'class': 'form-control'}),
                                       help_text='The column containing the username')
    password_col = forms.ChoiceField(label='Password Column', initial=5, choices=choices,
                                   widget=forms.Select(attrs={'class': 'form-control'}),
                                   help_text='The column containing the password')


    def clean(self):
        data = self.cleaned_data
        f = data.get('excel_file', None)
        ext = splitext(f.name)[1][1:].lower()
        if not ext in ["xlsx", "xls"]:
            raise forms.ValidationError(("the File type is not accepted"))
        return data


class OrderUploadForm(forms.Form):
    sheetChoice = (
        ('1', 'sheet1'),
        ('2', 'sheet2'),
        ('3', 'sheet3'),
        ('4', 'sheet4'),
        ('5', 'sheet5'),
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
    farmer_reference_col = forms.ChoiceField(label='Farmer ID / Phone number Column', initial=0, choices=choices,
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        help_text='The column containing the Farmers SYSTEM ID/Phone Number')
    farmer_name_col = forms.ChoiceField(label='Farmer Name Column', initial=1, choices=choices,
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        help_text='The column containing the Farmers Name')
    item_col = forms.ChoiceField(label='Item Column', initial=2, choices=choices,
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        help_text='The column containing the Item')
    quantity_col = forms.ChoiceField(label='Quantity Column', initial=3, choices=choices,
                                 widget=forms.Select(attrs={'class': 'form-control'}),
                                 help_text='The column containing the Quantity')
    order_date_col = forms.ChoiceField(label='Order Date Column', initial=4, choices=choices,
                                     widget=forms.Select(attrs={'class': 'form-control'}),
                                     help_text='The column containing the Order Date')


class CollectionUploadForm(forms.Form):
    sheetChoice = (
        ('1', 'sheet1'),
        ('2', 'sheet2'),
        ('3', 'sheet3'),
        ('4', 'sheet4'),
        ('5', 'sheet5'),
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
    farmer_reference_col = forms.ChoiceField(label='Farmer ID / Phone number Column', initial=0, choices=choices,
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        help_text='The column containing the Farmers SYSTEM ID/Phone Number')
    farmer_name_col = forms.ChoiceField(label='Farmer Name Column', initial=1, choices=choices,
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        help_text='The column containing the Farmers Name')
    product_col = forms.ChoiceField(label='Product Column', initial=2, choices=choices,
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        help_text='The column containing the Product')
    quantity_col = forms.ChoiceField(label='Quantity Column', initial=3, choices=choices,
                                 widget=forms.Select(attrs={'class': 'form-control'}),
                                 help_text='The column containing the Quantity')
    collection_date_col = forms.ChoiceField(label='Collection Date Column', initial=4, choices=choices,
                                     widget=forms.Select(attrs={'class': 'form-control'}),
                                     help_text='The column containing the Collection Date')


class FinancialInstitutionForm(forms.ModelForm):
    class Meta:
        model = FinancialInstitution
        fields = '__all__'


class OffTakerForm(forms.ModelForm):
    class Meta:
        model = OffTaker
        fields = '__all__'


class OrderFilterForm(forms.Form):
    name = forms.CharField(label='Name', max_length=150, required=False)
    phone_number = forms.CharField(max_length=150, required=False)
    product = forms.ChoiceField(widget=forms.Select(), choices=[], required=False)
    farmer_group = forms.ChoiceField(widget=forms.Select(), choices=[], required=False)
    district = forms.ChoiceField(widget=forms.Select(), choices=[], required=False)
    start_date = forms.CharField(max_length=150, required=False)
    end_date = forms.CharField(max_length=150, required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OrderFilterForm, self).__init__(*args, **kwargs)

        items = Item.objects.all()
        qs = CooperativeMember.objects.values('farmer_group__id', 'farmer_group__name').distinct()
        d_qs = CooperativeMember.objects.values('district__id', 'district__name').distinct()
        choices = [['', 'Farmer Group']]
        item_choices = [['', 'Item']]
        for q in qs:
            choices.append([q['farmer_group__id'], q['farmer_group__name']])
        for i in items:
            item_choices.append([i.id, i.name])
        self.fields['farmer_group'].choices = choices
        self.fields['product'].choices = item_choices
        if not self.request.user.profile.is_union():
            self.fields.pop('cooperative')


bootstrapify(OrderFilterForm)
bootstrapify(OrderUploadForm)
bootstrapify(OffTakerForm)
bootstrapify(FinancialInstitutionForm)
bootstrapify(CollectionUploadForm)
bootstrapify(AgentUploadForm)
bootstrapify(AgentForm)
bootstrapify(AgentUpdateForm)
bootstrapify(FarmerGroupForm)
bootstrapify(FarmerGroupUploadForm)
bootstrapify(AgentSearchForm)
bootstrapify(MemberOrderForm)
bootstrapify(OrderItemForm)
bootstrapify(CooperativeForm)
bootstrapify(MemberUploadForm)
bootstrapify(CooperativeUploadForm)
bootstrapify(CooperativeSharePriceForm)
bootstrapify(MemberProfileForm)
bootstrapify(CooperativeContributionForm)
bootstrapify(CooperativeShareTransactionForm)
bootstrapify(MemberSubscriptionForm)
bootstrapify(MemberSharesForm)
bootstrapify(MemberProfileSearchForm)
bootstrapify(CollectionForm)
bootstrapify(CollectionFilterForm)
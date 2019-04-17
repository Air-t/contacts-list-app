from django import forms
from django.core.validators import FileExtensionValidator, EmailValidator, RegexValidator
from .models import Person, Email, Address, Group, Phone, PHONE_CHOICES, EMAIL_CHOICES


class PersonForm(forms.ModelForm):
    name = forms.CharField(label='Name')
    surname = forms.CharField(label='Last Name')
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '5'}),
                                  label='Contact Description')
    photo = forms.ImageField(required=False, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])],
                             label='Contact Photo',
                             help_text="Allowed extensions: jpg, png."
                             )

    class Meta:
        model = Person
        fields = ('name', 'surname', 'description', 'photo')


class ShortPersonForm(forms.ModelForm):
    name = forms.CharField(label='Name')
    surname = forms.CharField(label='Last Name')

    class Meta:
        model = Person
        fields = ('name', 'surname')


class EmailForm(forms.ModelForm):
    email = forms.EmailField(validators=[EmailValidator()], label='Email')
    email_type = forms.IntegerField(label='Email Type',
                                    widget=forms.Select(choices=EMAIL_CHOICES))

    class Meta:
        model = Email
        fields = ('email', 'email_type')


class PhoneForm(forms.ModelForm):
    number = forms.CharField(validators=[RegexValidator(r'^(\+\d{2})?(\d{9})$')],
                             label='Phone Number')
    number_type = forms.IntegerField(label='Phone Type',
                                     widget=forms.Select(choices=PHONE_CHOICES))

    class Meta:
        model = Phone
        fields = ('number', 'number_type')


class AddressForm(forms.ModelForm):
    city = forms.CharField(label='City')
    street = forms.CharField(label='Street')
    home_no = forms.CharField(label='Home Number')
    apartment_no = forms.CharField(label='Apartment Number')
    zip_code = forms.IntegerField(validators=[RegexValidator(r'^(\d{2})\-?(\d{3})$')],
                                  label='Zip Code')

    class Meta:
        model = Address
        fields = ('city', 'street', 'home_no', 'apartment_no', 'zip_code')


class GroupForm(forms.ModelForm):
    name = forms.CharField(label='Group Name', required=True)

    class Meta:
        model = Group
        fields = ('name',)


class SelectGroupForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="")

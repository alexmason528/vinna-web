from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from server.account.models import Account
#from .models import Post


class DownloadForm(forms.Form):
    email = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': _('Email or Phone #')}))
    member = forms.CharField(required=False, widget=forms.HiddenInput())

    def is_valid(self):
      valid = super(DownloadForm, self).is_valid()
      if valid:
        return True
      else:
        return False



class UserForm(forms.ModelForm):

    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': _('Email')}))
    password = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': _('Password')}))
    password_confirm = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': _('Re-enter Password')}))
    first_name = forms.CharField(label='first_name', required=True, widget=forms.TextInput(attrs={'placeholder': _('First Name')}))
    last_name = forms.CharField(label='last_name', required=True, widget=forms.TextInput(attrs={'placeholder': _('Last Name')}))

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def is_valid(self):
        valid = super(UserForm, self).is_valid()

        if not valid:
            print('invalid UserForm')
            return valid

        cleaned_data = super(UserForm, self).clean()
    
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            self.add_error('password_confirm', 'Password does not match.')

        if self._errors:
          return False
        else:    
          return True


    def save(self, commit=True):
      try:
        email = self.cleaned_data['email']
        firstname = self.cleaned_data['first_name']
        lastname = self.cleaned_data['last_name']
        new_user = User.objects.create_user(username=email, email=email)
        new_user.first_name = firstname
        new_user.last_name = lastname

  #      user = super(MyRegistrationForm, self).save(commit=False)
        #user.email = self.cleaned_data['email']
        #user.username = user.email;
        new_user.set_password(self.cleaned_data['password'])

        if commit:
            new_user.save()

        return new_user
      except (ValueError, TypeError):
        print('failed')
        return



class AccountForm(forms.ModelForm):
    dob_month = forms.IntegerField(label='Month', required=True, widget=forms.NumberInput(attrs={'placeholder': _('Month')}))
    dob_day = forms.IntegerField(label='Day', required=True, widget=forms.NumberInput(attrs={'placeholder': _('Day')}))
    dob_year = forms.IntegerField(label='Year', required=True, widget=forms.NumberInput(attrs={'placeholder': _('Year')}))
    phone = forms.CharField(label='phone', required=True, widget=forms.TextInput(attrs={'placeholder': _('Phone Number')}))
#    language = forms.ChoiceField(label='language', required=True, choices=(('1','English'),('2','Español')))

    class Meta:
        model = Account
        fields = ('language', 'first_name', 'last_name', 'dob_year', 'dob_day', 'dob_month')

    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
        return cleaned_data

    def is_valid(self):
        # run the parent validation first
        valid = super(AccountForm, self).is_valid()
        valid = True

        # we're done now if not valid
        if not valid:
            print('invalid AccountForm')
            return valid

        cleaned_data = super(AccountForm, self).clean()

        dob_month = cleaned_data.get('dob_month')
        if dob_month < 1 and dob_month > 12:
            self.add_error('dob_month', _('Month is invalid'))

        dob_day = cleaned_data.get('dob_day')
        if dob_day < 1 and dob_day > 31:
            self.add_error('dob_day', _('Day is invalid'))

        dob_year = cleaned_data.get('dob_year')
        if dob_year < 1900 and dob_year > 2015:
            self.add_error('dob_year', _('Year is invalid'))

        print(self._errors)

#        try:
#            AccountForm.dob = datetime(dob_year, dob_month, dob_day)
#        except (ValueError, TypeError):
#            self.add_error('dob', _('DOB is invalid'))

        if self._errors:
            return False
        else:
          return True


    def save(self, commit=True):
            user = super(MyRegistrationForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            # user.set_password(self.cleaned_data['password1'])

            if commit:
                user.save()

            return user

from django import forms
from db.models import Inscription, Member


class InscriptionForm(forms.ModelForm):

    class Meta:
        model = Inscription
        fields = ('university', 'education', 'year')


class MemberForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.SelectDateWidget(), required=False, label="Date de naissance", localize=True)

    class Meta:
        model = Member
        fields = ('name', 'family_name', 'email', 'phone', 'cin', 'address',
                  'username', 'birthday')

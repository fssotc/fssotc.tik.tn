from django import forms
from db.models import Inscription, Member


class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ('name', 'family_name', 'email', 'phone')


class InscriptionForm(forms.ModelForm):

    class Meta:
        model = Inscription
        fields = ('university', 'education')

from django import forms
from db.models import Inscription, Member


class InscriptionForm(forms.ModelForm):

    class Meta:
        model = Inscription
        fields = ('member', 'university', 'education', 'year', 'inscription_num')


"""
class InscriptionForm(forms.Form):
    UNIVERSITY_CHOICES = (
        ("FSS", "Faculté des Sciences de Sfax"),
        ("ENIS", "Ecole Nationale des Ingénieurs de Sfax"),
        ("ISIMS", "Institut Supérieur d'Informatique et de Multimédia de Sfax"),
        ("ENETCOM", "Ecole Nationale d'electronique et de télécommunications de Sfax"),
        ("FSEGS", "Faculté des Sciences Economiques et de Gestion de Sfax"),
        ("IPEIS", "Institut Préparatoire aux Etudes d'Ingénieurs de Sfax"),
        ("", "Autre..."),
    )
    EDUCATION_CHOICES = (
        ("LF", "Licence Fondamentale"),
        ("LA", "Licence Appliqué"),
        ("P", "Préparatoire"),
        ("ENG", "Ingéniorat"),
        ("MR", "Master de Recherche"),
        ("MP", "Master Professionnel"),
        ("PHD", "Doctorat"),
        ("", "Autre..."),
    )
    YEAR_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
    )
    name = forms.CharField(label="Prénom / Name", max_length=100, min_length=3)
    family_name = forms.CharField(label="Nom / Family Name", max_length=100, min_length=3)
    email = forms.EmailField(label="E-mail")
    phone = forms.IntegerField(label="Phone", required=False)
    address = forms.CharField(label="Addresse / Address", max_length=400, required=False)
    username = forms.CharField(label="GitHub userame", max_length=50)
    birthday = forms.DateField(label="Date de naissance / Birthday", required=False, localize=True)
    inscription_num = forms.IntegerField(label="Inscription Num", required=False)
    university = forms.ChoiceField(label="Institution / University", choices=UNIVERSITY_CHOICES)
    education = forms.ChoiceField(label="Cycle", choices=EDUCATION_CHOICES)
    year = forms.ChoiceField(label="Année", choices=YEAR_CHOICES)
"""

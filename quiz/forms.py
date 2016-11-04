from django import forms
import django.forms

import docutils.core
import docutils.io


class _html(str):

    def __html__(self):
        return self


class _yes(_html):

    def __bool__(self):
        return True


class _not(_html):

    def __bool__(self):
        return False


def _rst(text):
    pub = docutils.core.Publisher(
        source_class=docutils.io.StringInput,
        destination_class=docutils.io.StringOutput,
    )
    pub.set_components(parser_name="rst", reader_name="standalone",
                       writer_name="html4css1")
    pub.get_settings(traceback=True, syntax_highlight='short')
    pub.set_source(source=text, source_path=None)
    pub.set_destination(None, None)
    pub.publish()
    html = ''.join(pub.writer.body)
    return _yes(html) if text else _not(html)


def _q(question, choices):
    choices = [(str(e[0]), _rst(e[1])) for e in enumerate(choices)]
    return forms.MultipleChoiceField(choices=choices, label=_rst(question),
                                     widget=forms.CheckboxSelectMultiple,
                                     required=False, label_suffix='')


class PythonQuizForm(forms.Form):
    q1 = _q('Python est une langue', (
        _yes('Dynamique'),
        _not('Typée'),
        _yes('Non typée'),
        _not("Statique"),
        _yes("Interprétée"),
        _not("Compilée"),
    ))
    q2 = _q('Extension du fichier source en Python', (
        _yes('``.py``'),
        _not('``.pyo``'),
        _not('``.pys``'),
        _not('``.python``'),
    ))
    q3 = _q('String multi-lignes peut être exprimé sans ``\\n`` avec', (
        _not("Single quotes"),
        _not("Double quotes"),
        _yes("Triple quotes"),
    ))
    q4 = _q('``//`` en python est', (
        _not("Commentaire"),
        _not("Commentaire multi-lignes"),
        _yes("Opérateur du division Int"),
        _not("Opérateur du division Float"),
        _not("Opérateur du division Double"),
    ))
    q5 = _q('''L'output de

.. code:: python

   print(r"""\\n1\\n2""")''', (
        _yes("``\\n1\\n2``"),
        _not("``12``"),
        _not("Aucune Correcte"),
    ))
    q6 = _q("On peut séparer multiple statements en même ligne en python avec", (
        _yes("``;``"),
        _not("``,``"),
        _not("``\\``"),
        _not("Non supporté"),
    ))

    q7 = _q("La fin d'un block est indiqué par le caractère", (
        _not("``;``"),
        _not("``\\``"),
        _not("``,``"),
        _yes("Aucun"),
    ))

    q8 = _q("``__str__`` est", (
        _yes("une méthode qui retourne une chaine représentant l'objet"),
        _not("une méthode qui affiche une chaine représentant  l'objet"),
        _not("une méthode qui converte l'objet à une chaine"),
        _yes("équivalant à ``toString()`` on Java"),
    ))

    q9 = _q("Pour vérifier le type d'un objet, on peut utiliser la fonction", (
        _yes("``type()``"),
        _not("``typeof()``"),
        _not("``instanceof()``"),
        _yes("``isinstance()``"),
        _not("``belongs()``"),
    ))

    q10 = _q('``pass`` est utiliser', (
        _yes("pour définir un block vide"),
        _not("pour retourner ``True``"),
        _not("pour retourner ``False``"),
        _not('comme équivalant du ``continue``'),
        _not('comme équivalant du ``break``'),
    ))

    q11 = _q("""Quelle est la valeur finale de la variable b

.. code:: python

    a = 7
    b = 12
    if a > 5:
        b = b - 4
    if b >= 10:
        b = b + 1""", (
        _not("``8``"),
        _not("``9``"),
        _not("``12``"),
        _yes("``13``"),
    ))

    def score(self):
        _sc = 0
        for f in self.cleaned_data:
            if f not in self.changed_data:
                continue
            correct = all(k in self.cleaned_data[f] if w
                          else k not in self.cleaned_data[f]
                          for k, w in self.fields[f].choices)
            _sc += 2 if correct else -2
        return _sc

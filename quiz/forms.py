from django import forms
import django.forms

import docutils.core
import docutils.io

from .models import Quiz, Question, Choice, Question, Submission, Answer
from db.models import Member


class _html(str):

    def __html__(self):
        return self


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
    return _html(''.join(pub.writer.body))


class CandidatForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ('email', 'username')


class QuizForm(forms.Form):

    def __init__(self, *args, instance=None, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.instance = instance
        self.max_score = 0
        choices = Choice.objects.filter(question__quiz=self.instance.quiz)[::1]
        for q in self.instance.quiz.question_set.all():
            cs = [c for c in choices if c.question_id == q.id]
            self.fields[str(q.pk)] = self.to_field(q, cs)
            self.max_score += q.score if not q.bonus else 0

    def to_field(self, q, cs):
        initial = []
        choices = []
        for c in cs:
            choices.append((str(c.pk), _rst(c.title)))
            try:
                a = self.instance.answer_set.get(choice=c)
                if a.value:
                    initial.append(c.pk)
            except:
                pass
        return forms.MultipleChoiceField(
            label=_rst(q.title),
            choices=choices, initial=initial,
            widget=forms.CheckboxSelectMultiple,
            required=False, label_suffix='')

    def save(self):
        for q in self.instance.quiz.question_set.all():
            for c in q.choice_set.all():
                v = str(c.pk) in self.cleaned_data[str(q.pk)]
                try:
                    a = self.instance.answer_set.get(choice__pk=c.pk)
                except:
                    a = Answer(submission=self.instance, choice=c)
                a.value = v
                a.save()

from django import forms
import django.forms
from django.db import transaction

import docutils.core
import docutils.io

from .models import Quiz, Question, Choice, Question, Submission, Answer
from db.models import Member


class _rst(str):
    _pub = docutils.core.Publisher(
        source_class=docutils.io.StringInput,
        destination_class=docutils.io.StringOutput,
    )
    _pub.set_components(parser_name="rst", reader_name="standalone",
                        writer_name="html4css1")
    _pub.get_settings(traceback=True, syntax_highlight='short')
    _pub.set_destination(None, None)

    def __html__(self):
        self._pub.set_source(source=self, source_path=None)
        self._pub.publish()
        return ''.join(self._pub.writer.body)


class CandidatForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ('email', 'username')


class QuizForm(forms.Form):

    def __init__(self, *args, instance=None, is_new=False, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.instance = instance
        self.max_score = 0
        self.is_new = is_new
        if self.is_new:
            choices = Choice.objects.filter(question__quiz=self.instance.quiz)[::1]
        else:
            answers = self.instance.answer_set.select_related('choice').all()[::1]
        for q in self.instance.quiz.question_set.all():
            if self.is_new:
                es = [c for c in choices if c.question_id == q.id]
            else:
                es = [a for a in answers if a.choice.question_id == q.id]
            self.fields[str(q.pk)] = self.to_field(q, es)
            self.max_score += q.score if not q.bonus else 0

    def to_field(self, q, es):
        initial = []
        choices = []
        if self.is_new:
            for c in es:
                choices.append((str(c.pk), _rst(c.title)))
        else:
            for a in es:
                choices.append((str(a.choice_id), _rst(a.choice.title)))
                if a.value:
                    initial.append(a.choice_id)
        return forms.MultipleChoiceField(
            label=_rst(q.title),
            choices=choices, initial=initial,
            widget=forms.CheckboxSelectMultiple,
            required=False, label_suffix='')

    def save(self):
        with transaction.atomic():
            self._save()

    def _save(self):
        if self.is_new:
            choices = Choice.objects.filter(
                question__quiz=self.instance.quiz)[::1]
            Answer.objects.bulk_create([Answer(
                submission=self.instance, choice=c,
                value=str(c.pk) in self.cleaned_data[str(c.question_id)])
                for c in choices])
        else:
            answers = self.instance.answer_set.select_related('choice').all()[::1]
            for a in answers:
                v = str(a.choice_id) in self.cleaned_data[
                    str(a.choice.question_id)]
                if a.value != v:
                    a.value = v
                    a.save(update_fields=['value'])

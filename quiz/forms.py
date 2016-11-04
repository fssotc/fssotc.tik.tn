from django import forms
import django.forms

import docutils.core
import docutils.io

from .models import Quiz, Question, Choice, Question, Submission


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


class QuizForm(forms.Form):

    def __init__(self, *args, instance=None, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.instance = instance
        self.max_score = 0
        for q in self.instance.quiz.question_set.all():
            self.fields[str(q.pk)] = self.to_field(q)
            self.max_score += q.score if not q.bonus else 0

    def to_field(self, q):
        return forms.MultipleChoiceField(
            label=_rst(q.title),
            choices=[(str(c.pk), _rst(c.title)) for c in q.choice_set.all()],
            widget=forms.CheckboxSelectMultiple,
            required=False, label_suffix='')

    def score(self):
        _sc = 0
        for f in self.changed_data:
            q = self.instance.quiz.question_set.get(pk=f)
            correct = all(str(c.pk) in self.cleaned_data[f]
                          if c.correct
                          else str(c.pk) not in self.cleaned_data[f]
                          for c in q.choice_set.all())
            _sc += q.score if correct else - q.score
        return _sc

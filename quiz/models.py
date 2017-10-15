from django.db import models
from django.urls import reverse
from django.contrib.sites.models import Site

from db.models import Member


class Quiz(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    start = models.DateTimeField(blank=True, null=True,
                                 verbose_name="Quiz Start Date (UTC)")
    end = models.DateTimeField(blank=True, null=True,
                               verbose_name="Quiz End Date (UTC)")
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('quiz', kwargs={'quiz_pk': self.pk})

    def max_score(self):
        return self.question_set.aggregate(
            models.Sum(models.F('score')))['score__sum']

    def questions_count(self):
        return self.question_set.count()


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    title = models.TextField()
    score = models.PositiveSmallIntegerField(default=2)
    bonus = models.BooleanField(default=False)
    position = models.PositiveSmallIntegerField("Position", null=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.TextField()
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Submission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.quiz, self.member)

    def score(self):
        sc = 0
        qs = self.quiz.question_set.all()[::1]
        answers = self.answer_set.select_related('choice').all()[::1]
        for q in qs:
            answered = False
            correct = True
            ans = [a for a in answers if a.choice.question_id == q.id]
            for a in ans:
                if a.value:
                    answered = True
                if a.value != a.choice.correct:
                    correct = False
            if answered:
                sc += q.score if correct else - q.score
        return sc

    def get_absolute_url(self):
        return reverse('submission', kwargs={
            'quiz_title': self.quiz.title,
            'member_email': self.member.email})


class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    value = models.BooleanField(default=False)

    def __str__(self):
        return "{}:{}".format(self.value, self.choice)

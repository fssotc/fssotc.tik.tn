from django.db import models

from db.models import Member


class Quiz(models.Model):
    title = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.title


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
        for q in self.quiz.question_set.all():
            answered = False
            correct = True
            for c in q.choice_set.all():
                a = self.answer_set.get(choice=c)
                if a.value:
                    answered = True
                if a.value != c.correct:
                    correct = False
            if answered:
                sc += q.score if correct else - q.score
        return sc


class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    value = models.BooleanField(default=False)

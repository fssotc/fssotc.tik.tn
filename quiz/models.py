from django.db import models

from db.models import Member


class Quiz(models.Model):
    title = models.CharField(max_length=200)

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


class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    value = models.BooleanField(default=False)

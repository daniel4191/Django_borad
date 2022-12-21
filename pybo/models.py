from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Question(models.Model):
    # author가 추가되었으니 views도 추가를 해줘야한다.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    # null은 데이터베이스상의 컬럼값(필드값이라고도 부른다.)의 공백 유무를 말하며
    # blank는 form.is_valid()로 유효성 검사를 할때 값 유무에 대해서 말한다.
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject


class Answer(models.Model):
    # author가 추가되었으니 views도 추가를 해줘야한다.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    # null은 데이터베이스상의 컬럼값(필드값이라고도 부른다.)의 공백 유무를 말하며
    # blank는 form.is_valid()로 유효성 검사를 할때 값 유무에 대해서 말한다.
    modify_date = models.DateTimeField(null=True, blank=True)

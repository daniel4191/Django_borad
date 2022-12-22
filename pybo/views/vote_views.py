from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from ..models import Question, Answer


# code line

@login_required(login_url='common:login')
def vote_question(request, question_id):
    """

    Submit pybo question recommendation
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, "you can't recommend yourself")

    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)


@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    """

    Submit pybo Answer comment
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, "you can't vote yourself")

    else:
        answer.voter.add(request.user)
    return redirect('pybo:detail', question_id=answer.question.id)

# question_create, question_modify, question_delete

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from ..models import Question
from ..forms import QuestionForm


# code line
# 비 로그인 상태에서는 User가 아니라 AnonymousUser가 들어가기 때문에 ValueError가 발생된다.
# 이를 방지하기 위해서 에너테이션을 써주는 것이다.
@login_required(login_url='common:login')
def question_create(request):
    """

    apply pybo question
    """

    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            # 임시저장, 만약 form에 바로 저장할 경우 create_date의 값이 설정되어있지 않기때문에
            # 오류가 발생된다.
            # 따라서 create_date가 정의 된 이후에 진짜 저장인 save()를 해준다.
            question = form.save(commit=False)
            question.author = request.user  # models에 추가된 author를 추가
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')

    else:
        # else니깐 request의 method가 GET인 경우다.
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """

    Edit pybo question
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, 'you don\'t have permission to edit')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)

    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """

    Delete pybo question
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "you don't have permission to delete")
        return redirect('pybo:detail', question_id=question.id)

    question.delete()
    return redirect('pybo:index')

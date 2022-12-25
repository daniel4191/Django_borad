# answer_create, answer_modify, answer_delete

from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from ..models import Question, Answer
from ..forms import AnswerForm

# code line

# 비 로그인 상태에서는 User가 아니라 AnonymousUser가 들어가기 때문에 ValueError가 발생된다.
# 이를 방지하기 위해서 에너테이션을 써주는 것이다.


@login_required(login_url='common:login')
def answer_create(request, question_id):
    """

    submit pybo answer
    """

    question = get_object_or_404(Question, pk=question_id)
    # 첫번째 인자로 등장하는 content, create_date는 모두 앱단위의 models의 데이터 구성요소와
    # 맞추기 위해서 필요하다
    # 여기서 answer_set이 쓰이는 이유는 models에서 Answer이 Question을 ForeignKey로 follow
    # 하고 있기 때문이다. 때문에 팔로우당하는클래스.포린키로따라가는클래스_set이 된다.
    # 그렇다면 왜 create일까?
    # question.answer_set.create(
    # 왜 사용방식이 POST.get('content')일까?
    # 요청값중에서.POST타입중에서.filter는 다양한수 혹은 값이 없어도 빈값을 리턴하니깐 반드시
    # 하나만 리턴해주는 get을 사용해서 content라는 값을 가지고 있는 것을 가져온다.
    # content=request.POST.get('content'), create_date=timezone.now())
    # 뒤에오는 question_id는 인자로 들어오니깐 그런다 치지만 앞인자의 question_id는 왜 question_id일까?
    # return redirect('pybo:detail', question_id=question_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # models에 추가된 author를 추가
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            # return redirect('pybo:detail', question_id=question.id)
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question.id), answer.id
            ))

    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """

    Edit pybo answer
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "you don't have permission to Edit")
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            # return redirect('pybo:detail', question_id=answer.question_id)
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail',
                            question_id=answer.question.id), answer.id
            ))

    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """

    Delete pybo answer
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "you don't have permission to Delete")
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

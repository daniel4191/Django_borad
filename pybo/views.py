from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Question, Answer, Comment
from .forms import QuestionForm, AnswerForm, CommentForm
# Create your views here.


def index(request):
    """

    print pybo lists
    """
    # 코드 2
    # 입력 인자
    # 여기서 get인자로 들어온 page는 request에 포함된 page를 의미하는 것이고
    # 이런 page인자에 대한 넘버가 없는 경우 자동 리턴값으로 1을 추가해준것
    page = request.GET.get('page', '1')  # page

    # 조회
    question_list = Question.objects.order_by('-create_date')

    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개의 포스트
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)

    # 코드 1
    # question_list = Question.objects.order_by('-create_date')
    # context = {'question_list': question_list}
    # return render(request, 'pybo/question_list.html', context)

# 이게 app단위의 urls로 보내지는 매핑용 인자다
# 물론 기본적으로는 동일한 앱단위 폴더 안에서만 매핑이 가능한거같다.


def detail(request, question_id):
    """

    print pybo contents
    """
    # 근본적으로 id로 지정된 question_id는 render를 통해서 html로 "보내지는"용도인듯 하다.
    # urls에서는 path에 지정해준 값에 의거하여 두번째 인자로 인하여서 question_id를 "가져오는"역할을 하는것 같다.
    # question = Question.objects.get(id=question_id)

    # 위의 것을 대체하기위해서 이렇게 해줬고, 에러가 생기는 페이지에 대해서는 404에러를 보내준다.
    question = get_object_or_404(Question, pk=question_id)
    # 여기의 question은 context를 통해서 render로 지정된 html파일로 태그를 보내준다.
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

# 여기에 인자로 오는 question_id가 필요한 이유는 어렴풋이는 알겠다.


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
            return redirect('pybo:detail', question_id=question.id)

    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


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
            return redirect('pybo:detail', question_id=answer.question_id)

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


@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    """

    Add pybo comment
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('pybo:detail', question_id=question.id)

    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """

    Edit pybo comment
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "you don't have permission to Edit comment")
        return redirect('pybo:detail', question_id=comment.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.question.id)

        else:
            form = CommentForm(instance=comment)
        context = {'form': form}
        return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    """

    Delete pybo comment
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "you don't have permission to delete")
        return redirect('pybo:detail', question_id=comment.question.id)

    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question.id)


@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    """

    Submit pybo answer's comment
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('pybo:detail', question_id=commit.answer.question.id)

    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    """

    Edit pybo answer comment
    """

    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(
            request, "you don't have permission to modify this comment")
        return redirect('pybo:detail', question_id=comment.answer.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)

    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    """

    Delete pybo answer comment
    """

    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(
            request, "you don't have permission to modify this comment")
        return redirect('pybo:detail', question_id=comment.answer.question.id)

    else:
        comment.delete()
    return render('pybo:detail', question_id=comment.answer.question.id)

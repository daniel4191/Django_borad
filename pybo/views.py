from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone

from .models import Question
from .forms import QuestionForm, AnswerForm
# Create your views here.


def index(request):
    """

    print pybo lists
    """
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)

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
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)

    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


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
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')

    else:
        # else니깐 request의 method가 GET인 경우다.
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

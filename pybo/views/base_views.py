# index, detail
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from ..models import Question


# code line

def index(request):
    """

    print pybo lists
    """
    # 코드 2
    # 입력 인자
    # 여기서 get인자로 들어온 page는 request에 포함된 page를 의미하는 것이고
    # 이런 page인자에 대한 넘버가 없는 경우 자동 리턴값으로 1을 추가해준것
    page = request.GET.get('page', '1')  # page
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')

    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')

    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    # 조회
    # question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            # 여기서 contains로 하게되면 대소문자를 구분해서 검색해주고
            # icontains로 하게되면 대소문자를 가리지 않고 검색해주는 역할을 한다.
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
            # distinct는 조회결과의 중복을 제거한후에 반환 한다
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개의 포스트
    page_obj = paginator.get_page(page)

    context = {
        'question_list': page_obj,
        'page': page,
        'kw': kw,
        'so': so
    }
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

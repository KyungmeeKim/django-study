from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from ..models import Question, Answer


# 페이징 표시 갯수
MAX_PAGE_CNT = 5
# 한페이지 내 게시물 갯수
MAX_LIST_CNT = 10




def index(request):
    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '')  # 검색어

    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목
            Q(content__icontains=kw) |  # 내용
            Q(author__username__icontains=kw) | #질문 글쓴이
            Q(answer__author__username__icontains=kw)   # 답변 글쓴이
        ).distinct()


    # 페이징 처리
    paginator = Paginator(question_list, MAX_LIST_CNT)
    page_obj = paginator.get_page(page)
    # 전체 페이지 마지막 번호
    last_page_num = 0
    for last_page in paginator.page_range:
        last_page_num = last_page_num + 1
    
    # 현재 페이지가 몇번째 블럭인지
    current_block = ((int(page)) -1 / MAX_PAGE_CNT) + 1
    current_block = int(current_block)

    # 페이지 시작번호
    page_start_number = ((current_block -1) * MAX_PAGE_CNT) + 1

    # 페이지 끝번호
    page_end_number = page_start_number + MAX_PAGE_CNT - 1

    context = {
        'question_list' : page_obj,
        'last_page_num' : last_page_num,
        'page_start_number' : page_start_number,
        'page_end_number' : page_end_number,
        'page' : page,
        'kw' :kw
    }

    return render(request, 'pybo/question_list.html', context)
        




def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, 'pybo/question_detail.html', context)
from django.shortcuts import get_object_or_404, redirect, render
from .models import Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.

# 페이징 표시 갯수
MAX_PAGE_CNT = 5
# 한페이지 내 게시물 갯수
MAX_LIST_CNT = 10

def index(request):
    page = request.GET.get('page', '1') # 페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, MAX_LIST_CNT)
    page_obj = paginator.get_page(page)
    #context = {'question_list': page_obj}
    #return render(request, 'pybo/question_list.html', context)
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
    }

    return render(request, 'pybo/question_list.html', context)

        

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render (request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)

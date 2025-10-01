from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from pybo.models import Question

import logging
logger = logging.getLogger('pybo')


def index(request):
    logger.info("INFO 레벨로 출력")
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    sort = request.GET.get('sort', 'recent')
    question_list = Question.objects.all()
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(answer__content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()
    # 정렬
    if sort == 'popular':
        question_list = question_list.annotate(num_answers=Count('answer')).order_by('-num_answers', '-create_date')
    else:  # 최신순
        question_list = question_list.order_by('-create_date')
    paginator = Paginator(question_list, 9)  # 9개씩(3열)
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'sort': sort}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
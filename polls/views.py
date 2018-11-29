from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse

from .models import Question, Choice


# Create your views here.
def index(request):
    """ 索引页 """
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list
    }

    # ex:4 render 是快捷函数，类似tp的助手函数
    return render(request, 'polls/index.html', context)

    # ex:3
    # template = loader.get_template('polls/index.html')
    # return HttpResponse(template.render(context, request))
    # ex:2
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)
    # ex:1
    # return HttpResponse("Hello, world.You'r at the polls index.")


def detail(request, question_id):
    """ 详情页 """
    # ex:2 get_object_or_404 快捷函数判断404，不存在就抛出Http404
    question = get_object_or_404(Question, pk=question_id)
    # ex:2 普通判断404方法
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exsit")
    return render(request, 'polls/detail.html', {'question': question})
    # ex:1
    # return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    """ 结果页 """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
    # ex:1
    # response = "You're looking at the result of question %s."
    # return HttpResponse(response % question_id)


def vote(request, question_id):
    """ 投票处理器 """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # 存现选项就投票次数加1,然后保存
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # ex:1
    # return HttpResponse("You're voting on question %s." % question_id)


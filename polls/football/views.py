
from django.shortcuts import render,get_object_or_404,render_to_response
from django.template import loader
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Sum

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from .models import Question,Choice

# def index(request):
#
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # output = ",".join([q.question_text for q in latest_question_list])
#     #
#     template = loader.get_template('football/index.html')
#     #
#     context = {'latest_question_list':latest_question_list,}
#     #
#     # # return HttpResponse(template.render(context,request))
#     # # return render(request,"football/index.html",context)
#     # return HttpResponse(output)
#
#     return HttpResponse(template.render(context, request))
#
#
# def detail(request,question_id):
#
#     question = get_object_or_404(Question, pk=question_id)
#     # return HttpResponse('Your are looking at question %s.' %question_id)
#     return render(request, 'football/detail.html',{'question':question})
#
# def result(request,question_id):
#
#     # return HttpResponse('Resulst')
#     question = get_object_or_404(Question,pk=question_id)
#
#     return render(request, 'football/results.html',{'question':question})

class IndexView(generic.ListView):

    template_name = "football/index.html"
    context_object_name = 'latest_question_list'

    # def get_queryset(self):
    #     return Question.objects.order_by('-pub_date')[:5]

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()

        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'football/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question

    template_name = 'football/results.html'

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)

        context['total_votes'] = context['object'].choice_set.aggregate(Sum('votes')).values()[0]


        return context



def vote(request,question_id):
    # return HttpResponse("Votes")

    question  = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):

        return render(request, 'football/detail.html',{
            'question' : question,
            'error_message': 'You didn"t select a choice',
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('football:results',args=(question.id,)))

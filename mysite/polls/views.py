from .models import *
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

def test(request):
    return render(request, 'map.html')

def index(request):
    question_list = Question.objects.order_by('-pub_date')[:5]
    #output = ', '.join([q.question_text for q in last_question_list])
    context = {'question_list': question_list}
    return render(request, 'index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question,id=question_id) #Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'detail.html', context)

def votes(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "선택된 값이 없습니다.",
            #'error_message': f"선택된 값이 없습니다. id ={request.POST['choice']}",
        })
    else:
        selected_choice.votes = F('votes')+1
        selected_choice.save()
        #return HttpResponseRedirect(reverse('questions:index'))
        return HttpResponseRedirect(reverse('questions:results',args=(question.id,)))
    
def results(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    context = {'question': question}
    return render(request, 'results.html', context)

class signupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('user_list')
    template_name = 'registration/signup.html'
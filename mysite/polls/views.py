from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.http import Http404
from django.db.models import F
from django.urls import reverse
from django.views import generic

class IndexView(generic.ListView):
    template_name="polls/index.html"
    context_object_name="lastest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model=Question
    template_name="polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name="polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message":"You didn't select a choice",
            },
        )
    else:
        selected_choice.votes=F("votes")+1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.http import Http404
from django.db.models import F
from django.urls import reverse

def index(request):
    lastest_question_list=Question.objects.order_by("-pub_date")[:5]
    template=loader.get_template("polls/index.html")
    context={
        "lastest_question_list": lastest_question_list,
    }
    return render(request, "polls/index.html", context)
# Create your views here.

def detail(request, question_id):
    try:
        question=Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question":question})

def results(request, question_id):
    response="You're looking at the results of question %s" % question_id
    return HttpResponse(response % question_id)

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

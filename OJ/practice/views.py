from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,Http404



from .models import Problem



def index(request):
    Problem_list = Problem.objects.order_by('problemid')
    context = {'Problem_list': Problem_list}
    return render(request, 'practice/index.html', context)
# Leave the rest of the views (detail, results, vote) unchanged



def detail(request, problemid):
    problem = get_object_or_404(Problem, pk=problemid)
    return render(request, 'practice/detail.html', {'problem': problem})

def results(request, problemid):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % problemid)

def submit(request, problemid):
    return HttpResponse("You're voting on question %s." % problemid)

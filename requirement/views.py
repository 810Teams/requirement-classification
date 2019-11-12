from django.shortcuts import render

from requirement.analyze import analyze
from requirement.entities import RequirementData


def index(request):
    ''' View Method: Index '''
    context = dict()

    if request.method == 'POST':
        title = request.POST.get('title')
        requirements = request.POST.get('requirements')

        context['data'] = analyze(RequirementData(title, requirements))

    return render(request, template_name='requirement/index.html', context=context)

from django.shortcuts import render

def index(request):
    ''' View Method: Index '''
    context = dict()
    return render(request, template_name='requirement/index.html', context=context)

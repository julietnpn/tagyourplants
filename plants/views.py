from django.shortcuts import render
from plants.models import Plant, PlantPost, TaxonomyPost
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.http import HttpResponse
from .forms import SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def homepage(request):
    return TemplateResponse(request, 'plants/index.html')

def search_form(request):
    return render(request, 'plants/plantResults.html')

def result_list(request):
    if('q' in request.GET):
        query = request.GET['q']
        plantResult = Plant.objects.filter(Q(common_name__icontains=query) | Q(scientific_name__icontains=query))
        search_id = set()
        for plant in plantResult:
            search_id.add(getattr(plant, 'plant_id'))
        return TemplateResponse(request,'plants/resultList.html', {'plantResult': plantResult, 'query': query})
    else:
        return HttpResponse(message)

def get_plant(request):
    if('q' in request.GET):
        query = request.GET['q']

    plantResult = Plant.objects.filter(Q(plant_id__exact=query))
    postResult = PlantPost.objects.filter(plant__plant_id=query).order_by('-score')

    paginator = Paginator(postResult, 1) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        postResult = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        postResult = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        postResult = paginator.page(paginator.num_pages)

    context = {
        "postResult": postResult,
        "plantResult": plantResult,
    }
    return TemplateResponse(request, 'plants/plantResults.html', context)

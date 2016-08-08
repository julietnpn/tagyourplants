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
        postResult = PlantPost.objects.filter(Q(plant__common_name__icontains=query) | Q(plant__scientific_name__icontains=query)).order_by('-score','plant_id')

        topResult_set = list()
        topPlant_set = set()
        for top in postResult:
            if (getattr(top, 'plant_id')) in topPlant_set:
                continue
            else:
                topPlant_set.add(getattr(top, 'plant_id'))
        #get the each plant_id
        for plant in topPlant_set:
            if plant:
                topPlant = PlantPost.objects.filter(Q(plant__plant_id__icontains=plant)).order_by('-score', 'plant_id')
                r = list(topPlant[:1])
                if r:
                    top_post = r[0]
                    topResult_set.append(getattr(top_post, 'post_id'))
                else:
                    top_post = None

        coverItem = PlantPost.objects.filter(pk__in = topResult_set)

        context = {
            'topPlant_set': topPlant_set,
            'query': query,
            'postResult': postResult,
            'top_post': top_post,
            'topResult_set': topResult_set,
            'coverItem': coverItem,
            'r': r,
            }
        return TemplateResponse(request,'plants/resultList.html', context)
    else:
        return HttpResponse(message)

def get_plant(request):
    if('q' in request.GET):
        query = request.GET['q']

    plantResult = Plant.objects.filter(Q(plant_id__exact=query))
    postResult = PlantPost.objects.filter(Q(plant__plant_id=query)).order_by('-score','post_id')

    #Pagination cause some duplicate!!!
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


# def get_post_by_tag(request):

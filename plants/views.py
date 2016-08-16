from django.shortcuts import render
from plants.models import Plant, PlantPost, TaxonomyPost
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseNotFound
from .forms import SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def homepage(request):
    return TemplateResponse(request, 'plants/index.html')

def search_form(request):
    return render(request, 'plantResults.html')

def result_list(request):
    if('q' in request.GET):
        query = request.GET['q']
#        postResult = PlantPost.objects.filter(Q(plant__common_name__icontains=query) | Q(plant__scientific_name__icontains=query)).order_by('-score','plant_id')
        postResult = PlantPost.objects.filter(Q(plant__common_name__iregex=query) | Q(plant__scientific_name__iregex=query)).order_by('-score','post_id')

        # if postResult == :
        #
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
                topPlant = PlantPost.objects.filter(Q(plant__plant_id__icontains=plant))
                #.order_by('-score', 'post_id')
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
    postResult = PlantPost.objects.filter(Q(plant__plant_id=query)).order_by('-score', 'post_id')


    firstPost, restPosts = postResult[0], postResult[1:]

    #
    # #Pagination cause some duplicate!!!
    # paginator = Paginator(postResult,25) # Show 25 contacts per page
    # page = request.GET.get('page')
    # try:
    #     postResult = paginator.page(page)
    # except PageNotAnInteger:
    # # If page is not an integer, deliver first page.
    #     postResult = paginator.page(1)
    # except EmptyPage:
    # # If page is out of range (e.g. 9999), deliver last page of results.
    #     postResult = paginator.page(paginator.num_pages)

    context = {
        "postResult": postResult,
        # "plantResult": plantResult,
        "firstPost": firstPost,
        "restPosts": restPosts,
    }
    return TemplateResponse(request, 'plants/plantResults.html', context)


def get_post_by_tag(request):
    if('tag' in request.GET):
        query = request.GET['tag']

        tagResult = PlantPost.objects.filter(Q(related_tag__icontains=query))
        idList = list()
        eachTagList = set()

        for t in tagResult:
            eachTagList = eval(getattr(t, 'related_tag'))
            if query in eachTagList:
                idList.append(getattr(t, 'post_id'))

        tagItem = PlantPost.objects.filter(pk__in = idList).order_by('post_date', 'post_id')

        paginator = Paginator(tagItem, 8) # Show 25 contacts per page
        page = request.GET.get('page')

        try:
            postResult = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            postResult = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            postResult = paginator.page(paginator.num_pages)

        if tagResult:
            context={
                "tagResult": tagResult,
                "query": query,
                "postResult": postResult,
                }
            return TemplateResponse(request, 'plants/tagResult.html', context)
        else:
            return HttpResponseNotFound

def get_singlepost_by_post_id(request):
    if('postID' in request.GET):
        query = request.GET['postID']
        singlePost = PlantPost.objects.filter(Q(post_id__exact=query))

    tag_list = set()
    for plant in singlePost:
        tag_list = eval(getattr(plant, 'related_tag'))

    if singlePost:
        context={
        "singlePost": singlePost,
        "query": query,
        "tag_list": tag_list,
                }
        return TemplateResponse(request, 'plants/singlePost.html', context)
    else:
        return HttpResponseNotFound

def gallary_for_each_plant(request):
    if('tag' in request.GET):
        query = request.GET['tag']
    plantPosts = PlantPost.objects.filter(Q(related_tag__iregex=query))


    firstPost, restPosts = plantPosts[0], plantPosts[1:]

    if plantPosts:
        context={
                "plantPosts": plantPosts,
                "firstPost": firstPost,
                "restPosts": restPosts,
                "query": query,
                }
        return TemplateResponse(request, 'plants/gallery.html', context)
    else:
        return HttpResponseNotFound

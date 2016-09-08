from django.shortcuts import render
from plants.models import Plant, PlantPost, TaxonomyPost
from django.db.models import Q
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseNotFound
from .forms import SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
# def homepage(request):
#     ordered_grid = PlantPost.objects.order_by('-score', '-post_date')[:30]
#     first = ordered_grid[3]
#     second = ordered_grid[5]
#     third = ordered_grid[8]
#     fourth = ordered_grid[11]
#     context = {
#         'ordered_grid': ordered_grid,
#         'first': first,
#         'second': second,
#         'third': third,
#         'fourth': fourth,
#     }
#
#     return TemplateResponse(request, 'plants/index.html', context)

def search_form(request):
    return render(request, 'plantResults.html')


def get_native_plant(request):
    nativePlant = Plant.objects.filter(Q(ca_native="TRUE")).order_by('common_name','plant_id')
    topResult_set = list()
    topPlant_set = set()
    if nativePlant:
        for top in nativePlant:
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
        count = len(coverItem)

        paginator = Paginator(coverItem, 8) # Show 25 contacts per page
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
            'nativePlant': nativePlant,
            'coverItem': coverItem,
            'count': count,
            'postResult': postResult,
            }
        return TemplateResponse(request,'plants/nativePlant.html', context)
    else:
        return render_to_response('plants/NoResult.html')

def result_list(request):
    if('q' in request.GET):
        query = request.GET['q']
        postResult = PlantPost.objects.filter(Q(plant__common_name__iregex=query) | Q(plant__scientific_name__iregex=query))
        topResult_set = list()
        topPlant_set = set()
        if postResult:
            for top in postResult:
                if (getattr(top, 'plant_id')) in topPlant_set:
                    continue
                else:
                    topPlant_set.add(getattr(top, 'plant_id'))
            #get the each plant_id
            for plant in topPlant_set:
                if plant:
                    topPlant = PlantPost.objects.filter(Q(plant__plant_id__icontains=plant)).order_by('-score', 'post_id')
                    r = list(topPlant[:1])
                    if r:
                        top_post = r[0]
                        topResult_set.append(getattr(top_post, 'post_id'))
                    else:
                        top_post = None

            coverItem = PlantPost.objects.filter(pk__in = topResult_set).order_by('-post_date')

            context = {
                'coverItem': coverItem,
                'postResult': postResult,
                'topPlant': topPlant,
                    }
            return TemplateResponse(request,'plants/resultList.html', context)
        else:
            return render_to_response('plants/NoResult.html')

def get_plant(request):
    if('q' in request.GET):
        query = request.GET['q']

    postResult = PlantPost.objects.filter(Q(plant__plant_id=query)).order_by('-score', 'post_id')
    firstPost, restPosts = postResult[0], postResult[1:]

    if postResult:
        context = {
            "postResult": postResult,
            "firstPost": firstPost,
            "restPosts": restPosts,
            }
        return TemplateResponse(request, 'plants/plantResults.html', context)
    else:
        return render_to_response('plants/NoResult.html')

def get_post_by_tag(request):
    try:
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

            count = len(tagItem)
            if tagItem:
                context={
                    "tagResult": tagResult,
                    "query": query,
                    "postResult": postResult,
                    "count": count,
                    }
                return TemplateResponse(request, 'plants/tagResult.html', context)
            else:
                return render_to_response('plants/NoResult.html')

    except ObjectDoesNotExist :
        return messages("No Data Found.")
# def get_post_by_taxono(request):
#     if('taxono' in request.GET):


def get_singlepost_by_post_id(request):
    if('postID' in request.GET):
        query = request.GET['postID']
        singlePost = PlantPost.objects.filter(Q(post_id__exact=query))
    else:
        return render_to_response('plants/NoResult.html')

    tag_list = set()
    for plant in singlePost:
        tag_list = eval(getattr(plant, 'related_tag'))

    if singlePost:
        context={
        "singlePost": singlePost,
        "tag_list": tag_list,
                }
        return TemplateResponse(request, 'plants/singlePost.html', context)
    else:
        return render_to_response('plants/NoResult.html')


def upVotes(request,post_id):
    singlePost = PlantPost.objects.filter(Q(post_id__exact=post_id))

    tag_list = set()
    for plant in singlePost:
        tag_list = eval(getattr(plant, 'related_tag'))

    if singlePost:
        context={
        "singlePost": singlePost,
        "tag_list": tag_list,
                }

    post = PlantPost.objects.get(pk=post_id)
    post.score += 1
    post.save()

    messages.success(request, 'Thanks for your feedback! ')
    return TemplateResponse(request, 'plants/voteCompleteNote.html', context)

def downVotes(request,post_id):

    singlePost = PlantPost.objects.filter(Q(post_id__exact=post_id))

    tag_list = set()
    for plant in singlePost:
        tag_list = eval(getattr(plant, 'related_tag'))

    if singlePost:
        context={
        "singlePost": singlePost,
        "tag_list": tag_list,
                }

    post = PlantPost.objects.get(pk=post_id)
    post.score -= 1
    post.save()

    messages.success(request, 'Thanks for your feedback! ')
    return TemplateResponse(request, 'plants/voteCompleteNote.html', context)

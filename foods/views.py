from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,Http404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from common.decorators import ajax_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from itertools import chain

# Create your views here.
from .models import Image,Comment
from .forms import ImageCreationForm,CommentForm
from actions.utils import create_action

def index(request):
    """the home page of foodie"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('foodie'))
    else:
        return render(request,'foods/guest_index.html')

@login_required
def foodie(request):
    following_ids = request.user.following.values_list('id',
                                                       flat=True)
    if request.method != 'POST':
        image_form = ImageCreationForm()
    else:
        image_form = ImageCreationForm(data=request.POST,files=request.FILES)
        if image_form.is_valid():
            new_image = image_form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            return HttpResponseRedirect(reverse('foodie'))
    image = Image.objects.all()
    posted_images = image.order_by('-created')
    paginator = Paginator(posted_images, 8)
    page = request.GET.get('page')
    try:
        posted_images = paginator.page(page)
    except PageNotAnInteger:
        posted_images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        posted_images =  paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,'foods/foodie_ajax.html',
                      {'posted_images':posted_images,'image_form':image_form})

    context = {'posted_images':posted_images,'image_form':image_form}
    return render(request,'foods/foodie.html',context)

@login_required
def foods_detail(request,id,slug):
    image = get_object_or_404(Image,id=id,slug=slug)
    comment = image.comments.all()
    comments = comment.order_by('-created')

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.image = image
            new_comment.user = request.user
            new_comment.save()
            return HttpResponseRedirect(reverse('foods_detail',args=(id,slug)))
    else:
        comment_form = CommentForm()

    context = {'image':image,'comment_form':comment_form,'comments':comment}

    return render(request,'foods/foods_detail.html',context)

@login_required
def post_delete(request,id,slug):
    image = get_object_or_404(Image,id=id,slug=slug)
    if image.user != request.user:
        raise Http404
    else:
        if request.method == 'POST':
            image.delete()
            return HttpResponseRedirect(reverse('your_profile'))

    return render(request,'foods/post_delete.html',{'image':image})

@ajax_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})

from django.shortcuts import render,reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Profile
from .forms import LoginForm,UserRegistrationForm, \
                    UserEditForm,ProfileEditForm
from .models import Profile,Contact
from actions.utils import create_action
from foods.models import Image

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('foodie'))
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request,'account/register_done.html',
                          {'new_user':new_user})

    else:
        user_form = UserRegistrationForm()

    return render(request,'account/register.html',{'user_form':user_form})

@login_required
def profile(request):
    user = request.user
    images = Image.objects.filter(user=request.user).order_by('-created')
    paginator = Paginator(images, 8)
    page = request.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,'account/profile_ajax.html',{'images':images,})

    context = {'user':user,'images':images,}
    return render(request,'account/profile.html',context)

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,'account/edit.html',
                  {'user_form':user_form,'profile_form':profile_form})


@login_required
def user_list(request):
    user = User.objects.filter(is_active=True)
    user_unordered = user.exclude(username=request.user)
    users = user_unordered.order_by('username')
    paginator = Paginator(users, 15)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        users = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,'account/user/user_list_ajax.html',{'users':users,})

    return render(request,'account/user/list.html',{'users':users})

@login_required
def user_detail(request,username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)

    posted_images = user.images_created.order_by('-created')
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
        return render(request,'account/user/user_detail_ajax.html',
                      {'posted_images':posted_images,'user':user})

    return render(request,'account/user/detail.html',{'user':user,'posted_images':posted_images,})

@login_required
@ajax_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})


@login_required
def connection(request):
    followers = request.user.followers.all()
    followings = request.user.following.all()

    context = {'followings':followings,'followers':followers}
    return render(request,'account/user/connections.html',context)

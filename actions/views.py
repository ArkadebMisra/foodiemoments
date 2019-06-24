
from django.shortcuts import render
from .models import Action
from foods.models import Image
# Create your views here.

def notification(request):
    # Display all actions by default
    following_ids = request.user.following.values_list('id',
                                                       flat=True)

    images = Image.objects.all()
    images_ids = images.filter(user=request.user).values_list('id',flat=True)
    actions = Action.objects.exclude(user=request.user)
    actions = actions.filter(target_id__in=images_ids)
    actions = actions.select_related('user', 'user__profile')\
                     .prefetch_related('target')[:10]
                     
    return render(request,'actions/notification.html',{'actions':actions,
                                                       'images_ids':images_ids})
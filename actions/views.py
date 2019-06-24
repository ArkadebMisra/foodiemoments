
from django.shortcuts import render
from .models import Action
from foods.models import Image
# Create your views here.

def notification(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',
                                                       flat=True)
    actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile')\
                     .prefetch_related('target')[:10]
    return render(request,'actions/notification.html',{'actions':actions)
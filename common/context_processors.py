from foods.models import Image


def post_count(request):
    if request.user.is_authenticated:
        post_no = Image.objects.filter(user=request.user).count()
    else:
        post_no = 0
    return {'post_no':post_no}

def followers_count(request):
    if request.user.is_authenticated:
        followers_no = request.user.following.count()
    else:
        followers_no = 0
    return {'followers_no':followers_no}

def following_count(request):
    if request.user.is_authenticated:
        following_no = request.user.followers.count()
    else:
        following_no = 0
    return {'following_no':following_no}


def showcase_posts(request):
    if request.user.is_authenticated:
        sw_images = Image.objects.filter(user=request.user).order_by('-created')[:4]
    else:
        sw_images = None
    return {'sw_images':sw_images}

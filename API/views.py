from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404
from datetime import timedelta, datetime
from django.db.models import Q


def clientIp(request):
    try:
        xForwardFor = request.META.get('HTTP_X_FORWARD_FOR')
        if xForwardFor:
            ip = xForwardFor.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    except:
        ip = ""
    return ip


@login_required
def home(request):
    if request.user.is_authenticated:
        if request.user.is_active:
            lastIp = request.user.profile.ip
        else:
            lastIp = ""
        currentIp = clientIp(request)
        if currentIp == lastIp:
            condIp = "It's the same IP address."
        else:
            condIp = "Warning! Different IP address."
    else:
        condIp = clientIp(request)
    allPosts = Post.objects.all().order_by('-datetime')
    return render(request, 'API/home.html', {'posts': allPosts, 'cond_ip': condIp})


@login_required
def newPost(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form = PostForm()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'API/newPost.html', {'form': form})


@login_required
def posts(request):
    response = []
    posts = Post.objects.filter().order_by('-datetime')
    for post in posts:
        response.append(
            {
                'datetime': post.datetime,
                'title': post.title,
                'content': post.content,
                'author': f"{post.user.first_name} {post.user.last_name}",
                'hash': post.hash,
                'txId': post.txId,
            }
        )
    return JsonResponse(response, safe=False)


@login_required
def lastHourPosts(request):
    response = []
    now = datetime.now()
    oneHourAgo = now - timedelta(hours=1)
    posts = Post.objects.filter(datetime__range=(oneHourAgo, now))
    for post in posts:
        response.append(
            {
                'datetime': post.datetime,
                'title': post.title,
                'content': post.content,
                'author': f"{post.user.first_name} {post.user.last_name}",
                'hash': post.hash,
                'txId': post.txId,
            }
        )
    return JsonResponse(response, safe=False)


@login_required
def search(request):
    query = request.GET.get('q')
    n = 0
    posts = Post.objects.filter(Q(content__contains=query) | Q(title__contains=query))
    for post in posts:
        if query:
            n += 1
    return HttpResponse(f"The word {query} appears {n} times in all posts")


@login_required
def countPost(response):
    userPosts = User.objects.annotate(total=Count('post'))
    return render(response, 'API/count.html', {'user_posts': userPosts})


@login_required
def userId(request, id):
    user = get_object_or_404(User, id=id)
    userPosts = Post.objects.filter(user=user).count()
    return render(request, 'API/userId.html', {'user': user, "user_posts": userPosts})

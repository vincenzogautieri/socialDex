from datetime import timedelta, datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q

from .models import Post
from .forms import PostForm


def client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    except Exception:
        ip = ""
    return ip


@login_required
def home(request):
    if request.user.is_active:
        last_ip = request.user.profile.ip
    else:
        last_ip = ""
    current_ip = client_ip(request)
    if current_ip == last_ip:
        cond_ip = "It's the same IP address."
    else:
        cond_ip = "Warning! Different IP address."
    all_posts = Post.objects.all().order_by('-datetime')
    return render(request, 'API/home.html', {'posts': all_posts, 'cond_ip': cond_ip})


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            post.write_on_chain()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'API/newPost.html', {'form': form})


def _serialize_post(post):
    return {
        'datetime': post.datetime,
        'title': post.title,
        'content': post.content,
        'author': f"{post.user.first_name} {post.user.last_name}".strip() or post.user.username,
        'hash': post.hash,
        'txId': post.tx_id,
    }


@login_required
def posts(request):
    all_posts = Post.objects.all().order_by('-datetime')
    response = [_serialize_post(post) for post in all_posts]
    return JsonResponse(response, safe=False)


@login_required
def last_hour_posts(request):
    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)
    recent_posts = Post.objects.filter(datetime__range=(one_hour_ago, now))
    response = [_serialize_post(post) for post in recent_posts]
    return JsonResponse(response, safe=False)


@login_required
def search(request):
    query = request.GET.get('q', '')
    matches = Post.objects.filter(Q(content__contains=query) | Q(title__contains=query))
    count = matches.count() if query else 0
    return HttpResponse(f"The word {query} appears {count} times in all posts")


@login_required
def count_post(request):
    user_posts = User.objects.annotate(total=Count('post'))
    return render(request, 'API/count.html', {'user_posts': user_posts})


@login_required
def user_id(request, id):
    user = get_object_or_404(User, id=id)
    posts_count = Post.objects.filter(user=user).count()
    return render(request, 'API/userId.html', {'user': user, 'user_posts': posts_count})

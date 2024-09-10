from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Post, Tag
from .forms import ThreadForm

# Create your views here.
def login_page(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except: 
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist.')

    context={}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect("home")


def home(request):

    q = request.GET.get("q") if "q" in request.GET else ""
    tag_name = request.GET.get("tag", "").upper() if "tag" in request.GET else ""

    print("request", request.GET)
    if tag_name != "":
        tag_value = getattr(Tag.TagType, tag_name, None)
        threads = Post.objects.filter(post_type="t").filter(tag__name=tag_value).prefetch_related('tag')
    elif q != "":
        threads = Post.objects.filter(post_type="t").filter(
            Q(title__icontains=q) | Q(content__icontains=q)).prefetch_related('tag')
    else: 
        threads = Post.objects.filter(post_type="t").prefetch_related('tag')
    tags = Tag.objects.all()

    threads_count = threads.count()
    context = {'threads': threads, 'tags': tags, 'threads_count': threads_count}
    return render(request, 'base/home.html', context=context)


def thread(request, thread_pk):
    p = request.GET.get("p") if "p" in request.GET else ""
    thread = Post.objects.get(post_id=thread_pk)

    if p != "":
        posts = Post.objects.filter(parent_post=thread_pk).filter(
            Q(title__icontains=p) | Q(content__icontains=p))
    else: 
        posts = Post.objects.filter(parent_post=thread_pk)

    posts_count = posts.count()
    context = {'thread': thread, 'posts': posts, 'posts_count': posts_count}

    return render(request, 'base/thread.html', context=context)


def post(request, thread_pk, post_pk):
    post = Post.objects.get(post_id=post_pk)
    thread = Post.objects.get(post_id=thread_pk)
    context = {'post': post, 'thread': thread}

    return render(request, 'base/post.html', context=context)

@login_required(login_url='login')
def create_thread(request):
    form = ThreadForm()

    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.post_type = 't'
            new_post.save()

            return redirect("home")

    context = {"form": form}
    return render(request, "base/thread_form.html", context)

@login_required(login_url='login')
def create_post(request):

    thread_pk = request.GET.get('thread')
    form = ThreadForm()

    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.post_type = 'p'
            new_post.parent_type = 't'
            new_post.parent_post = Post.objects.get(post_id=thread_pk)
            new_post.save()

            return redirect("thread", thread_pk=thread_pk)

    context = {"form": form}
    return render(request, "base/thread_form.html", context)

@login_required(login_url='login')
def update_thread(request, thread_pk):
    thread = Post.objects.get(post_id=thread_pk)
    form = ThreadForm(instance=thread)

    if request.user != thread.author:
        return HttpResponse('You are not allowed here!!')

    if request.method == "POST":
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/thread_form.html', context=context)

@login_required(login_url='login')
def update_post(request, post_pk):

    thread_pk = request.GET.get('thread')
    post = Post.objects.get(post_id=post_pk)
    form = ThreadForm(instance=post)

    if request.user != post.author:
        return HttpResponse('You are not allowed here!!')

    if request.method == "POST":
        form = ThreadForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("thread", thread_pk=thread_pk)

    context = {'form': form}
    return render(request, 'base/thread_form.html', context=context)

@login_required(login_url='login')
def delete_post(request, post_pk):
    try: 
        thread_pk = request.GET.get('thread')
    except:
         thread_pk=None

    post = Post.objects.get(post_id=post_pk)

    if request.user != post.author:
        return HttpResponse('You are not allowed here!!')

    if request.method == "POST":
        post.delete()

        if thread_pk is not None:
            return redirect("thread", thread_pk=thread_pk)
        else:
            return redirect('home')
    return render(request, "base/delete.html", {'obj': post})


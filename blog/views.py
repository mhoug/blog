from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm


def post_list(request):
    last_post = Post.objects.latest('pk')
    posts = Post.objects.filter(pk__lte=last_post.pk, pk__gt=last_post.pk - 10).order_by('-pk')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_all(request):
    last_post = Post.objects.latest('pk')
    posts = Post.objects.filter(pk__lte=last_post.pk).order_by('-pk')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    last_post = Post.objects.latest('pk')
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post, 'last_post': last_post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

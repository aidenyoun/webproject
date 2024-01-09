from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

def forum(request):
    posts = Post.objects.all()
    return render(request, 'forum/forum.html', {'posts': posts})

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            if request.is_ajax():  # Ajax 요청인 경우
                return JsonResponse({'message': '게시글이 성공적으로 추가되었습니다.'})
            else:  # Ajax 요청이 아닌 경우
                return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'forum/post_new.html', {'form': form})

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'forum/post_edit.html', {'form': form})

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'forum/post_delete.html', {'post': post})

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return JsonResponse({'message': 'Success'})
        else:
            return JsonResponse({'message': 'Form is not valid'})
    else:
        return JsonResponse({'message': 'Not a POST request'})

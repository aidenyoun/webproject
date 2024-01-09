import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser

def forum(request, category=None):
    if category:
        posts = Post.objects.filter(category=category)
    else:
        posts = Post.objects.all().order_by('-created_at')
    return render(request, 'forum/forum.html', {'posts': posts})

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_new(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        form = PostForm(data)
        if form.is_valid():
            post = form.save()
            if request.is_ajax():
                return JsonResponse({'message': '게시글이 성공적으로 추가되었습니다.', 'pk': post.pk})
            else:
                return redirect('post_detail', pk=post.pk)
        else:
            errors = {field: error.get_json_data() for field, error in form.errors.items()}
            if request.is_ajax():
                return JsonResponse({'message': '모든 필드를 채워주세요.', 'errors': errors})
            else:
                return render(request, 'forum/post_new.html', {'form': form})
    else:
        form = PostForm()
        if request.is_ajax():
            return JsonResponse({'message': 'Form is ready', 'form': form.as_p()})
        else:
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
            return JsonResponse({'message': 'Success', 'pk': post.pk})
        else:
            return JsonResponse({'message': 'Form is not valid', 'errors': form.errors.as_json()})
    else:
        return JsonResponse({'message': 'Not a POST request'})

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'forum/post_detail.html', {'post': post})

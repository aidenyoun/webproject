import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, UserProfile, Comment
from .forms import PostForm, CommentForm
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from django.contrib import messages


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
            post = form.save(commit=False)
            post.author = request.user  # 현재 로그인한 사용자를 게시물의 작성자로 설정
            post.save()
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
            post = form.save(commit=False)
            post.author = request.user
            post.save()
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

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_view(request):
    # 'GET' 요청 처리는 필요에 따라 구현해야 합니다.
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 현재 로그인한 사용자를 게시물의 작성자로 설정
            post.save()
            return JsonResponse({'message': 'Success', 'pk': post.pk})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'message': 'Form is not valid', 'errors': errors})
    else:
        # 'GET' 요청에 대한 처리가 필요하다면 여기에 구현합니다.
        return JsonResponse({'message': 'Not a POST request'})

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 페이지 로드 시 조회수 증가
    post.views += 1
    post.save()

    # 현재 로그인한 사용자가 각 댓글을 추천했는지 확인
    comments = Comment.objects.filter(post=post)
    comments_user_has_liked = [comment.pk for comment in comments if comment.is_liked_by_user(request.user)]

    context = {
        'post': post,
        'comments_user_has_liked': comments_user_has_liked,
    }
    return render(request, 'forum/post_detail.html', context)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def recommend_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user_profile = UserProfile.objects.get(user=request.user)

    # 사용자가 자신의 게시글을 추천하려는 경우를 방지
    if post.author != request.user:
        # 이미 추천한 게시글인지 확인
        if post.liked_users.filter(id=request.user.id).exists():
            messages.error(request, '이미 이 게시물을 추천하셨습니다.')
        else:
            post.liked_users.add(request.user)
            post.likes += 1
            post.save()
            messages.success(request, '게시물을 추천하셨습니다.')

    return redirect('forum:post_detail', pk=post.pk)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_new(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        text = request.POST['text']
        comment = Comment.objects.create(post=post, author=request.user, text=text)
        return redirect('forum:post_detail', pk=post.pk)
    else:
        return render(request, 'forum/comment_new.html', {'post': post})

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def recommend_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.is_liked_by_user(request.user):
        # 사용자가 이미 추천한 경우
        messages.error(request, '이미 이 댓글을 추천하셨습니다.')
    else:
        # 사용자가 추천하지 않았을 경우
        comment.liked_users.add(request.user)
        messages.success(request, '댓글을 추천하셨습니다.')
    return redirect('forum:post_detail', pk=comment.post.pk)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            return redirect('forum:post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'forum/comment_edit.html', {'form': form})

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('forum:post_detail', pk=post_pk)
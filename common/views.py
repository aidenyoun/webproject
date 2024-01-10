from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from common.forms import UserForm
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

def logout_view(request):
    logout(request)
    return redirect('main')
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('main')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)

        # 로그인 처리.
        login(request, user)

        # 사용자가 성공적으로 로그인하면 토큰을 생성하거나 가져옵니다.
        token, created = Token.objects.get_or_create(user=user)
        # 토큰 키를 응답으로 반환합니다.
        return Response({"token": token.key}, status=status.HTTP_200_OK)
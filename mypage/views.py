from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect, render
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def mypage(request):
    user = request.user
    return render(request, 'mypage/mypage.html', {'user': user})

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # 비밀번호 변경 후 세션 유지
            request.session['alert'] = '변경 성공!'
            return redirect('main')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'mypage/password_change.html', {'form': form})


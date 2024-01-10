from django.shortcuts import render

def main(request):
    alert = request.session.pop('alert', None)  # 세션에서 알림 메시지를 가져오고 삭제
    return render(request, 'main/main.html', {'alert': alert})


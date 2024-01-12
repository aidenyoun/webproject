from django.shortcuts import render
from django.db.models import Q
from .models import Medicine

def search(request):
    return render(request, 'search/search.html')

def name_search(request):
    query = request.GET.get('q')
    results = []
    message = ""
    if query:  # query 값이 유효한지 확인
        # 정확히 일치하는 결과를 먼저 찾습니다.
        results = Medicine.objects.filter(name=query)
        if not results:  # 일치하는 결과가 없다면 유사한 결과를 찾습니다.
            results = Medicine.objects.filter(name__icontains=query)
            if results:
                message = "정확한 이름을 찾지 못했지만, 유사한 결과를 찾았습니다."
        if not results:  # 유사한 결과도 없다면 메시지를 설정합니다.
            message = "약품명을 다시 확인해주세요!"

    return render(request, 'search/name_search.html', {'results': results, 'message': message})
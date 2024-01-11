from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from datetime import datetime
from .models import Medicine
from .forms import MedicineForm
from django.views.decorators.csrf import csrf_exempt
import datetime


def manage(request):
    if request.user.is_authenticated:
        medicines = Medicine.objects.filter(user=request.user)
    else:
        medicines = Medicine.objects.none()
    return render(request, 'manage/manage.html', {'medicines': medicines})

def calendar(request):
    context = {
        'current_year': datetime.now().year,
        'current_month': datetime.now().month,
    }
    return render(request, 'manage/calendar.html', context)

def manage_medicine(request):
    if request.method == 'POST':
        # 각 필드별로 검증
        if not request.POST['medicine_name']:
            messages.error(request, '약품 이름을 입력해주세요.')
            return render(request, 'manage/manage_medicine.html')
        if not request.POST['medicine_form']:
            messages.error(request, '약품 형태를 입력해주세요.')
            return render(request, 'manage/manage_medicine.html')
        if not request.POST['start_date']:
            messages.error(request, '시작 날짜를 입력해주세요.')
            return render(request, 'manage/manage_medicine.html')
        if not request.POST['end_date']:
            messages.error(request, '종료 날짜를 입력해주세요.')
            return render(request, 'manage/manage_medicine.html')

        start_date = datetime.strptime(request.POST['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(request.POST['end_date'], "%Y-%m-%d").date()

        if start_date > end_date:
            messages.error(request, '끝일자는 시작일자보다 빨라야 합니다.')
            return render(request, 'manage/manage_medicine.html')

        # 약품 정보 저장
        medicine = Medicine()
        medicine.user = request.user
        medicine.name = request.POST['medicine_name']
        medicine.form = request.POST['medicine_form']
        medicine.start_date = start_date
        medicine.end_date = end_date

        # 체크박스가 체크되었을 때만 시간 값을 저장
        if 'morning_check' in request.POST:
            medicine.morning_time = request.POST.get('morning_time', None)
        if 'lunch_check' in request.POST:
            medicine.lunch_time = request.POST.get('lunch_time', None)
        if 'dinner_check' in request.POST:
            medicine.dinner_time = request.POST.get('dinner_time', None)

        medicine.save()

        messages.success(request, '저장되었습니다.')
        return redirect('/manage')
    else:
        # 현재 로그인한 사용자의 약품 정보만 가져와서 context에 추가
        medicines = Medicine.objects.filter(user=request.user)
        return render(request, 'manage/manage_medicine.html', {'medicines': medicines})


def edit_medicine(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if id is None:
            return HttpResponseBadRequest("Invalid request: id is missing.")
        try:
            id = int(id)
        except ValueError:
            return HttpResponseBadRequest("Invalid request: id is not a number.")
        medicine = get_object_or_404(Medicine, id=id, user=request.user)
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manage:manage'))
    else:
        id = request.GET.get('id')
        if id is None:
            return HttpResponseBadRequest("Invalid request: id is missing.")
        try:
            id = int(id)
        except ValueError:
            return HttpResponseBadRequest("Invalid request: id is not a number.")
        medicine = get_object_or_404(Medicine, id=id, user=request.user)
        form = MedicineForm(instance=medicine)
    return render(request, 'manage/edit_medicine.html', {'form': form, 'medicine': medicine})

def delete_medicine(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        medicine = get_object_or_404(Medicine, id=id)
        medicine_name = medicine.name
        medicine.delete()
        return JsonResponse({'status': 'OK', 'deleted_medicine': medicine_name})

@csrf_exempt
def get_medications(request):
    if request.method == 'POST':
        date = request.POST['date']  # 클라이언트에서 보낸 날짜를 가져옵니다.
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()  # 문자열을 날짜 객체로 변환합니다.

        # 해당 날짜에 해당 사용자가 복용해야 하는 약의 목록을 가져옵니다.
        medicines = Medicine.objects.filter(user=request.user, start_date__lte=date, end_date__gte=date)
        medicine_list = []
        for medicine in medicines:
            medicine_list.append(medicine.name)

        # 약의 목록을 JSON 형식으로 반환합니다.
        return JsonResponse({'medicines': medicine_list})
from django.shortcuts import render, redirect, get_object_or_404
from manage.models import Medicine
from django.utils import timezone

def main(request):
    if request.user.is_authenticated:
        medicines = Medicine.objects.filter(user=request.user)
    else:
        medicines = None  # 비회원인 경우 medicines는 None으로 설정

    alert = request.session.pop('alert', None)
    return render(request, 'main/main.html', {'alert': alert, 'medicines': medicines})

def save_medication(request):
    if request.method == 'POST':
        medication_name = request.POST['medication_name']
        morning = 'morning' in request.POST
        lunch = 'lunch' in request.POST
        dinner = 'dinner' in request.POST
        today_date = timezone.now().date()

        try:
            # 오늘 날짜의 해당 약물을 찾습니다.
            medicine = Medicine.objects.get(
                user=request.user,
                name=medication_name,
            )
        except Medicine.DoesNotExist:
            # 약물이 없으면 새로 생성합니다.
            medicine = Medicine.objects.create(
                user=request.user,
                name=medication_name,
                date=today_date,
            )

        # 복용 기록을 저장합니다.
        if morning:
            medicine.morning_dose = True
            medicine.morning_dose_time = timezone.now()
        if lunch:
            medicine.lunch_dose = True
            medicine.lunch_dose_time = timezone.now()
        if dinner:
            medicine.dinner_dose = True
            medicine.dinner_dose_time = timezone.now()
        medicine.save()

        return redirect('/')

from django.shortcuts import render, redirect, get_object_or_404
from manage.models import Medicine
from django.utils import timezone

def main(request):
    # 사용자의 약품 리스트를 가져옵니다.
    medicines = Medicine.objects.filter(user=request.user)

    alert = request.session.pop('alert', None)  # 세션에서 알림 메시지를 가져오고 삭제
    # 'medicines'를 context에 추가하여 템플릿에 전달합니다.
    return render(request, 'main/main.html', {'alert': alert, 'medicines': medicines})

def save_medication(request):
    if request.method == 'POST':
        medication_name = request.POST['medication_name']
        morning = 'morning' in request.POST
        lunch = 'lunch' in request.POST
        dinner = 'dinner' in request.POST

        # 약품 이름으로 기존 객체를 가져옵니다.
        # 해당하는 객체가 없다면 새로운 객체를 생성합니다.
        medicine, created = Medicine.objects.get_or_create(
            user=request.user,
            name=medication_name,
            defaults={
                'morning_dose': morning,
                'lunch_dose': lunch,
                'dinner_dose': dinner
            }
        )

        # 객체가 새로 생성된 것이 아니라면, 복용 시간을 업데이트합니다.
        if not created:
            medicine.morning_dose = morning
            medicine.lunch_dose = lunch
            medicine.dinner_dose = dinner

            if morning:
                medicine.morning_dose_time = timezone.now()

            if lunch:
                medicine.lunch_dose_time = timezone.now()

            if dinner:
                medicine.dinner_dose_time = timezone.now()

            medicine.save()

        return redirect('/')

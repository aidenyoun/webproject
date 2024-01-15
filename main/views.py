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
        medicine, created = Medicine.objects.get_or_create(
            user=request.user,
            name=medication_name,
            date=timezone.now().date(),
            defaults={
                'morning_dose': morning,
                'lunch_dose': lunch,
                'dinner_dose': dinner
            }
        )
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

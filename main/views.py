from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Medicine, MedicineDose
from django.utils import timezone
from django.shortcuts import get_object_or_404

def main(request):
    if request.user.is_authenticated:
        medicines = Medicine.objects.filter(user=request.user)
        medicine_doses = {medicine: [dose.dose_time for dose in MedicineDose.objects.filter(medicine=medicine)] for medicine in medicines}
    else:
        medicines = None
        medicine_doses = None
    alert = request.session.pop('alert', None)
    return render(request, 'main/main.html', {'alert': alert, 'medicines': medicines, 'medicine_doses': medicine_doses})

def save_medication(request, medication_id):
    if request.method == 'POST':
        medicine_name = request.POST.get('name', '')
        morning = 'morning_dose_taken' in request.POST
        afternoon = 'afternoon_dose_taken' in request.POST
        evening = 'evening_dose_taken' in request.POST
        today_date = timezone.now().date()

        medicine, created = Medicine.objects.get_or_create(
            id=medication_id,
            defaults={'name': medicine_name},
        )

        if morning:
            MedicineDose.objects.update_or_create(
                medicine=medicine,
                dose_time='morning',
                defaults={
                    'dose_taken': True,
                    'dose_taken_time': timezone.now(),
                },
            )
        else:
            MedicineDose.objects.update_or_create(
                medicine=medicine,
                dose_time='morning',
                defaults={
                    'dose_taken': False,
                    'dose_taken_time': None,
                },
            )

        if afternoon:
            MedicineDose.objects.update_or_create(
                medicine=medicine,
                dose_time='afternoon',
                defaults={
                    'dose_taken': True,
                    'dose_taken_time': timezone.now(),
                },
            )
        else:
            MedicineDose.objects.update_or_create(
                medicine=medicine,
                dose_time='afternoon',
                defaults={
                    'dose_taken': False,
                    'dose_taken_time': None,
                },
            )

        if evening:
            MedicineDose.objects.update_or_create(
                medicine=medicine,
                dose_time='evening',
                defaults={
                    'dose_taken': True,
                    'dose_taken_time': timezone.now(),
                },
            )
        else:
            MedicineDose.objects.update_or_create(
                medicine=medicine,
                dose_time='evening',
                defaults={
                    'dose_taken': False,
                    'dose_taken_time': None,
                },
            )
        return redirect('/')

@csrf_exempt
def get_medications(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        medicines = Medicine.objects.filter(user=request.user, date=date)
        medicines_list = [medicine.name for medicine in medicines]
        return JsonResponse({'medicines': medicines_list})
    else:
        return JsonResponse({'error': 'Invalid Method'})

def medication_view(request):
    medicines = Medicine.objects.all()
    medicine_doses = {medicine: [dose.dose_time for dose in MedicineDose.objects.filter(medicine=medicine)] for medicine in medicines}

    context = {
        'medicines': medicines,
        'medicine_doses': medicine_doses,
    }

    return render(request, 'main/main.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from datetime import datetime as dt
from .models import Medicine
from .forms import MedicineForm
from django.views.decorators.csrf import csrf_exempt
import datetime


def manage(request):
    medicines = Medicine.objects.filter(user=request.user) if request.user.is_authenticated else Medicine.objects.none()
    return render(request, 'manage/manage.html', {'medicines': medicines})

def calendar(request):
    context = {
        'current_year': datetime.datetime.now().year,
        'current_month': datetime.datetime.now().month,
    }
    return render(request, 'manage/calendar.html', context)

def manage_medicine(request):
    if request.method == 'POST':
        fields = ['medicine_name', 'medicine_form', 'start_date', 'end_date']
        for field in fields:
            if not request.POST[field]:
                messages.error(request, f'{field}을 입력해주세요.')
                return render(request, 'manage/manage_medicine.html')

        start_date = dt.strptime(request.POST['start_date'], "%Y-%m-%d").date()
        end_date = dt.strptime(request.POST['end_date'], "%Y-%m-%d").date()

        if start_date > end_date:
            messages.error(request, '끝일자는 시작일자보다 빨라야 합니다.')
            return render(request, 'manage/manage_medicine.html')

        medicine = Medicine(user=request.user, name=request.POST['medicine_name'], form=request.POST['medicine_form'],
                            start_date=start_date, end_date=end_date)

        for time in ['morning', 'lunch', 'dinner']:
            if f'{time}_check' in request.POST:
                setattr(medicine, f'{time}_time', request.POST.get(f'{time}_time', None))

        medicine.save()

        messages.success(request, '저장되었습니다.')
        return redirect('/manage')
    else:
        medicines = Medicine.objects.filter(user=request.user)
        return render(request, 'manage/manage_medicine.html', {'medicines': medicines})

def edit_medicine(request):
    id = request.POST.get('id') if request.method == 'POST' else request.GET.get('id')
    if id is None:
        return HttpResponseBadRequest("Invalid request: id is missing.")
    try:
        id = int(id)
    except ValueError:
        return HttpResponseBadRequest("Invalid request: id is not a number.")
    medicine = get_object_or_404(Medicine, id=id, user=request.user)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manage:manage'))
    else:
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
        date_str = request.POST.get('date')
        date = dt.strptime(date_str, "%Y-%m-%d").date()
        medicines = Medicine.objects.filter(user=request.user, date=date)
        medicines_list = [medicine.name for medicine in medicines]
        return JsonResponse({'medicines': medicines_list})
    else:
        return JsonResponse({'error': 'Invalid Method'})

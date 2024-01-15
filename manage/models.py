from django.db import models

class Medicine(models.Model):
    MEDICINE_TYPE_CHOICES = [
        ('tablet', '정제'),
        ('capsule', '캡슐'),
        ('liquid', '액제'),
        ('other', '기타'),
    ]

    NOTIFY_TIME_CHOICES = [
        ('morning', '아침'),
        ('lunch', '점심'),
        ('dinner', '저녁'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    form = models.CharField(max_length=20)
    date = models.DateField(null=True)  # 날짜 정보 기록
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    morning_time = models.TimeField(null=True, blank=True)
    lunch_time = models.TimeField(null=True, blank=True)
    dinner_time = models.TimeField(null=True, blank=True)  # 알림 시간
    morning_dose = models.BooleanField(default=False)  # 아침 복용 여부
    lunch_dose = models.BooleanField(default=False)  # 점심 복용 여부
    dinner_dose = models.BooleanField(default=False)  # 저녁 복용 여부
    morning_dose_time = models.DateTimeField(null=True, blank=True)  # 아침 복용 시간
    lunch_dose_time = models.DateTimeField(null=True, blank=True)  # 점심 복용 시간
    dinner_dose_time = models.DateTimeField(null=True, blank=True)  # 저녁 복용 시간

    def __str__(self):
        return self.name

class MedicineDose(models.Model):
    DOSE_TIME_CHOICES = [
        ('morning', '아침'),
        ('lunch', '점심'),
        ('dinner', '저녁'),
    ]

    medicine = models.ForeignKey('Medicine', on_delete=models.CASCADE, related_name='doses')
    dose_time = models.CharField(max_length=10, choices=DOSE_TIME_CHOICES)
    dose_taken = models.BooleanField(default=False)
    dose_taken_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('medicine', 'dose_time')


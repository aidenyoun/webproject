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
    start_date = models.DateField()
    end_date = models.DateField()
    morning_time = models.TimeField(null=True, blank=True)
    lunch_time = models.TimeField(null=True, blank=True)
    dinner_time = models.TimeField(null=True, blank=True)  # 알림 시간

    def __str__(self):
        return self.name

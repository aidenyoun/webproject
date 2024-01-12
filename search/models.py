from django.db import models

class Medicine(models.Model):
    name = models.CharField(max_length=200) # 약품명
    description = models.TextField() # 약품 설명
    image = models.ImageField(upload_to='medicines/', blank=True, null=True) # 약품 사진

    def __str__(self):
        return self.name
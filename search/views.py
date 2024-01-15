from django.shortcuts import render
from django.views import View
from keras.models import load_model
from io import BytesIO
from keras.preprocessing import image
import numpy as np
from .models import Medicine
import base64
import os

def search(request):
    return render(request, 'search/search.html')

def name_search(request):
    query = request.GET.get('q')
    results = []
    message = ""
    if query:
        results = Medicine.objects.filter(name=query)
        if not results:
            results = Medicine.objects.filter(name__icontains=query)
            if results:
                message = "정확한 이름을 찾지 못했지만, 유사한 결과를 찾았습니다."
        if not results:
            message = "약품명을 다시 확인해주세요!"

    return render(request, 'search/name_search.html', {'results': results, 'message': message})

def decode_predictions(preds, top=1):
    top_classes = preds[0].argsort()[-top:][::-1]

    return top_classes

class PicSearchView(View):
    def get(self, request):
        return render(request, 'search/pic_search.html')

    def post(self, request):
        img_file = request.FILES.get('drug_image')
        message = ''
        medicine_info = None

        if img_file:
            model = load_model('models/Intel_image_classification_model.h5')
            img_data = img_file.read()
            img_io = BytesIO(img_data)
            img = image.load_img(img_io, target_size=(150, 150))
            x = image.img_to_array(img)
            print('Image data:', x)  # 이미지 데이터 출력

            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)

            preds = model.predict(x)
            print('Prediction:', preds)  # 예측값 출력

            medicine_index = np.argmax(preds)

            index_to_name = {
                0: '게루삼정',
                1: '리단정(탄산리튬)',
                2: '마이암부톨제피정',
                3: '셉트린정',
                4: '키모랄에스정',
                5: '후릭스정(푸로세미드)',
                6: '부광메티마졸정',
                7: '싸이메트정',
                8: '일양노이시린에이정(규산알루민산마그네슘)',
                9: '네오메디코푸정',
            }

            medicine_name = index_to_name[medicine_index]

            try:
                medicine = Medicine.objects.get(name=medicine_name)
            except Medicine.DoesNotExist:
                message = '해당하는 약품을 찾을 수 없습니다.'
            else:
                medicine_info = {
                    'name': medicine.name,
                    'description': medicine.description,
                    'image_name': os.path.basename(medicine.image.name) if medicine.image else None,
                }
        else:
            message = '이미지 파일을 업로드해주세요.'

        context = {
            'medicine_info': medicine_info,
            'message': message,
        }

        response = render(request, 'search/pic_search.html', context)
        response['Cache-Control'] = 'no-store'
        return response
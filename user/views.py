import jwt
import json
import requests

from django.views import View
from django.http import JsonResponse

from config.settings import (
    SECRET_KEY,
    ALGORITHM
)

from .models import Users
from .utils import login_decorator

KAKAO_API = 'https://kapi.kakao.com/v2/user/me'

class SocialLoginView(View):
    def post(self, request):
        try:
            kakao_token         = request.headers['Authorization']
            req_kakao_profile   = requests.get(KAKAO_API,headers = {
                'Authorization' : f'Bearer {kakao_token}'
            })
            profile         = req_kakao_profile.json()
            kakao_email     = profile['kakao_account']['email']
            kakao_id        = profile['properties']['nickname']
            kakao_picture   = profile['properties']['profile_image']

            if Users.objects.filter(email = kakao_email).exists():
                token = jwt.encode({'email' : kakao_email}, SECRET_KEY, algorithm=ALGORITHM)
                token = token.decode('utf-8')
                return JsonResponse({
                    'access_token'      : token,
                    'nickname'          : kakao_id,
                    'profile_image'     : kakao_picture,
                    'email'             : kakao_email
                }, status=200)

            Users(
                email           = kakao_email,
                kakao_id        = kakao_id,
                picture         = kakao_picture,
            ).save()

            token = jwt.encode({'email' : kakao_email}, SECRET_KEY, algorithm=ALGORITHM)
            token = token.decode('utf-8')

            return JsonResponse({
                'access_token'      : token,
                'nickname'          : kakao_id,
                'profile_image'     : kakao_picture,
                'email'             : kakao_email
            }, status=200)

        except KeyError:
                return JsonResponse({'Message' : 'INVALID_KEYS'}, status=400)

    @login_decorator
    def get(self, request):
        return JsonResponse({
            'email'         : request.userinfo.email,
            'nickname'      : request.userinfo.kakao_id,
            'profile_image' : request.userinfo.picture
        }, status = 200)

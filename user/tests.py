import json

from django.test import (
    TestCase,
    Client,
)
from unittest.mock import (
    patch,
    MagicMock
)
from .models import User

class SocialLoginTest(TestCase):
    def setUp(self):
        User.objects.create(
            email           = 'test@test.com',
            kakao_id        = 'test',
            picture         = 'http://k.kakaocdn.net/dn/5w8QS/btqCrOP9kx6/XcCLekEj4OrEbCncK7CLiK/img_640x640.jpg'
        )
    def tearDown(self):
        User.objects.filter(email='test@test.com').delete()

    @patch('user.views.requests')
    def test_login_pass(self, mocked_request):

        class MockedResponse:
            def json(self):
                return {
                    'kakao_account' : {
                        'email' : 'test@test.com'
                    },
                    'properties' : {
                        'nickname'      : 'test',
                        'profile_image' : 'http://k.kakaocdn.net/dn/5w8QS/btqCrOP9kx6/XcCLekEj4OrEbCncK7CLiK/img_640x640.jpg'
                    }
                }

        mocked_request.get = MagicMock(return_value = MockedResponse())

        kakao_id = MockedResponse().json()['properties']['nickname']
        kakao_picture = MockedResponse().json()['properties']['profile_image']
        kakao_email = MockedResponse().json()['kakao_account']['email']

        client  = Client()
        headers = {
            'HTTP_Authorization'    : '',
            'content_type'          : 'application/json'
        }
        response = client.post('/user/login', **headers)
        token = response.json()['access_token']

        self.assertEqual(response.json(), {
            'access_token'  : token,
            'nickname'      : kakao_id,
            'profile_image' : kakao_picture,
            'email'         : kakao_email
        })
        self.assertEqual(response.status_code, 200)

    @patch('user.views.requests')
    def test_login_fail(self, mocked_request):

        class MockedResponse:
            def json(self):
                return {
                    'account' : {
                        'email' : 'test@test.com'
                    },
                    'properties' : {
                        'nickname'  : 'test',
                        'image'     : 'http://k.kakaocdn.net/dn/5w8QS/btqCrOP9kx6/XcCLekEj4OrEbCncK7CLiK/img_640x640.jpg'
                    }
                }

        mocked_request.get = MagicMock(return_value = MockedResponse())

        client  = Client()
        headers = {
            'HTTP_Authorization'    : '',
            'content_type'          : 'application/json'
        }
        response = client.post('/user/login', **headers)

        self.assertEqual(response.json(),{
            'Message' : 'INVALID_KEYS'
        })
        self.assertEqual(response.status_code, 400)

from django.conf import settings
from django.contrib.auth import login
import requests


class FacebookClient:

    client_id = settings.FACEBOOK_CLIENT_ID
    secret_key = settings.FACEBOOK_SECRET_KEY
    user_info_fields = 'id'
    redirect_uri = 'http://localhost:8000/login/social/facebook/callback'

    token_url = 'https://graph.facebook.com/v7.0/oauth/access_token'
    profile_url = 'https://graph.facebook.com/v7.0/me'

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    # 인증 토큰 발급
    def get_access_token(self, code):
        res = requests.get(self.token_url, params = {'code': code, 'client_id': self.client_id, 'client_secret': self.secret_key, 'redirect_uri': self.redirect_uri})
        return res.ok, res.json()

    # 프로필 얻기
    def get_profiles(self, access_token):
        res = requests.get(self.profile_url, params = {'fields': self.user_info_fields, 'access_token': access_token})
        return res.ok, res.json()
    


class FacebookLoginMixin:
    facebook_client = FacebookClient()

    def login_with_facebook(self, code):
        # 인증 토큰 발급
        is_success, token_infos = self.facebook_client.get_access_token(code)
        if not is_success:
            return False, '다시 로그인 해주십시오.'
        
        access_token =  token_infos.get('access_token'),
        token_type = token_infos.get('token_type'),
        expires_in = token_infos.get('expires_in')

        is_success, profile = self.get_facebook_profiles(access_token)
        if not is_success:
            return False, '다시 로그인 해주십시오.'

        # 유저 생성 또는 업데이트
        user, created = self.model.objects.get_or_create(uid='social//facebook/' + str(profile.get('id')))
        if created:
            user.set_password(None)
        user.is_social = True
        user.save()

        # 세션데이터 추가
        self.set_session(access_token=access_token, expires_in=expires_in, token_type=token_type, uid='social//facebook/' + str(profile.get('id')))

        return True, user

    def get_facebook_profiles(self, access_token):
        is_success, profile = self.facebook_client.get_profiles(access_token)
        if not is_success:
            return False, '다시 로그인 해주십시오.'
            

        return True, profile

            

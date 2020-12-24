from django.conf import settings
from django.contrib.auth import login
import requests


class GoogleClient:
    client_id = settings.GOOGLE_CLIENT_ID
    secret_key = settings.GOOGLE_SECRET_KEY
    grant_type = 'authorization_code'
    redirect_uri = 'http://localhost:8000/login/social/google/callback'

    token_url = 'https://oauth2.googleapis.com/token'
    profile_url = 'https://www.googleapis.com/oauth2/v3/userinfo'

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def get_access_token(self, code):
        res = requests.post(self.token_url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, params={'code': code, 'client_id': self.client_id, 'client_secret': self.secret_key, 'redirect_uri': self.redirect_uri, 'grant_type': self.grant_type})
        return res.ok, res.json()

    def get_profile(self, access_token):
        res = requests.get(self.profile_url, params={'access_token': access_token})
        return res.ok, res.json()

class GoogleLoginMixin:
    google_client = GoogleClient()

    def login_with_google(self, code):
        # 인증토큰 발급
        is_success, token_infos = self.google_client.get_access_token(code)
        if not is_success:
            return False, '다시 로그인 해주십시오.'
            
        access_token = token_infos.get('access_token')
        expires_in = token_infos.get('expires_in')
        id_token = token_infos.get('id_token')
        scope = token_infos.get('scope')
        token_type = token_infos.get('token_type')
        refresh_token = token_infos.get('refresh_token')

        # 구글 프로필 얻기
        is_success, profiles = self.get_google_profiles(access_token)
        if not is_success:
            return False, '다시 로그인 해주십시오.'

        # 유저 생성 또는 업데이트
        user, created = self.model.objects.get_or_create(uid='social//google/' + str(profiles.get('sub')))
        if created:
            user.set_password(None)
        user.is_social = True
        user.save()

        # 세션데이터 추가
        self.set_session(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in, token_type=token_type, uid='social//google/' + str(profiles.get('sub')))

        return True, user

    def get_google_profiles(self, access_token):
        is_success, profiles = self.google_client.get_profile(access_token)

        if not is_success:
            return False, '다시 로그인 해주십시오.'
        
        return True, profiles



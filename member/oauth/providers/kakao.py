from django.conf import settings
from django.contrib.auth import login
import requests

class KakaoClient:
    client_id = settings.KAKAO_CLIENT_ID
    secret_key = settings.KAKAO_SECRET_KEY
    grant_type = 'authorization_code'
    redirect_uri = 'http://localhost:8000/login/social/kakao/callback'

    token_url = 'https://kauth.kakao.com/oauth/token'
    profile_url = 'https://kapi.kakao.com/v2/user/me'

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def get_access_token(self, code):
        res = requests.get(self.token_url, params={'grant_type': self.grant_type, 'client_id': self.client_id, 'redirect_uri': self.redirect_uri, 'code': code})
        return res.ok, res.json()

    def get_profile(self, access_token, token_type="Bearer"):
        res = requests.get(self.profile_url, headers={'Authorization': '{} {}'.format(token_type, access_token)})
        return res.ok, res.json()


class KakaoLoginMixin:
    kakao_client = KakaoClient()

    def login_with_kakao(self, code):

        # 인증토큰 발급
        is_success, token_infos = self.kakao_client.get_access_token(code)
        if not is_success:
            return False, '다시 로그인 해주십시오.'

        access_token = token_infos.get('access_token')
        expires_in = token_infos.get('expires_in')
        refresh_token = token_infos.get('refresh_token')
        refresh_token_expires_in = token_infos.get('refresh_token_expires_in')
        token_type = token_infos.get('token_type')
        error = token_infos.get('error')

        # 카카오 프로필 얻기
        is_success, profiles = self.get_kakao_profile(access_token, token_type)
        if not is_success:
            return False, profiles

        # 유저 생성 또는 업데이트
        user, created = self.model.objects.get_or_create(uid='social//kakao/' + str(profiles.get('id')))
        if created:
            user.email = profiles.get('kakao_account').get('email')
            user.name = profiles.get('kakao_account').get('profile').get('nickname')
            user.set_password(None)
            user.is_social = True
            user.save()

        # 세션데이터 추가
        self.set_session(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in, token_type=token_type, uid='social//kakao/' + str(profiles.get('id')))

        return True, user

        
    def get_kakao_profile(self, access_token, token_type):
        is_success, profiles = self.kakao_client.get_profile(access_token, token_type)

        if not is_success:
            return False, '다시 로그인 해주십시오.'
        
        return True, profiles



        
        

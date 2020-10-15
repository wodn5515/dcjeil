from django.conf import settings
from django.contrib.auth import login
import requests

class NaverClient:
    client_id = settings.NAVER_CLIENT_ID
    secret_key = settings.NAVER_SECRET_KEY
    grant_type = 'authorization_code'

    token_url = 'https://nid.naver.com/oauth2.0/token'
    profile_url = 'https://openapi.naver.com/v1/nid/me'

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def get_access_token(self, state, code):
        res = requests.get(self.token_url, params={'client_id': self.client_id, 'client_secret': self.secret_key, 'grant_type': self.grant_type, 'state': state, 'code': code})
        return res.ok, res.json()

    def get_profile(self, access_token, token_type='Bearer'):
        res = requests.get(self.profile_url, headers={'Authorization': '{} {}'.format(token_type, access_token)}).json()

        if res.get('resultcode') != '00':
            return False, res.get('message')
        else:
            return True, res.get('response')
            
class NaverLoginMixin:
    naver_client = NaverClient()

    def login_with_naver(self, state, code):

        # 인증토큰 발급
        is_success, token_infos = self.naver_client.get_access_token(state, code)
        if not is_success:
            return False, '{} [{}]'.format(token_infos.get('error_description'), token_infos.get('error'))

        access_token = token_infos.get('access_token')
        refresh_token = token_infos.get('refresh_token')
        expires_in = token_infos.get('expires_in')
        token_type = token_infos.get('token_type')

        # 네이버 프로필 얻기
        is_success, profiles = self.get_naver_profile(access_token, token_type)
        if not is_success:
            return False, profiles
        
        # 유저 생성 또는 업데이트
        user, created = self.model.objects.get_or_create(email = profiles.get('email'))
        if created:
            user.uid='social//naver/'+profiles.get('id')
            user.name = profiles.get('name')
            user.set_password(None)
            user.is_social = True
            user.save()

        # 세션데이터 추가
        self.set_session(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in, token_type=token_type, uid='social//naver/' + str(profiles.get('id')))

        return True, user

    def get_naver_profile(self, access_token, token_type):
        is_success, profiles = self.naver_client.get_profile(access_token, token_type)

        if not is_success:
            return False, profiles

        return True, profiles
from django.conf import settings
from django.contrib.auth import login


class NaverClient:
    
    def get_access_token(self, state, code):
        return True

class NaverLoginMixin:
    naver_client = NaverClient()

    def login_with_naver(self, state, code):

        # 인증토큰 발급
        is_success, token_infos = self.naver_client.get_access_token(state, code)
        if not is_success:
            return False, '{} [{}]'.format(token_infos.get('error_desc'), token_infos.get('error'))

        access_token = token_infos.get('access_token')
        refresh_token = token_infos.get('refresh_token')
        expires_in = token_infos.get('expires_in')
        token_type = token_infos.get('token_type')

        # 네이버 프로필 얻기
        is_success, profiles = self.get_naver_profile(access_token, token_type)
        if not is_success:
            return False, profiles
        
        # 유저 생성 또는 업데이트
        
        
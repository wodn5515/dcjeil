function buildQuery(params){
    return Object.keys(params).map(function(key){return key + '=' + encodeURIComponent(params[key])}).join('&')
}

function buildUrl(baseUrl, query){
    return baseUrl + '?' + buildQuery(query)
}

function naverLogin(){ // 네이버 로그인
    params = {
        response_type: 'code',
        client_id: 'e4ZsoJAd0lfPVJQldldH',
        redirect_url: location.origin + '/login/social/naver/callback' + location.search,
        state: document.querySelector('input[name=csrfmiddlewaretoken]').value
    }
    url = buildUrl('https://nid.naver.com/oauth2.0/authorize', params)
    location.replace(url)
}

function kakaoLogin(){ // 카카오 로그인
    params = {
        response_type: 'code',
        client_id: '67e7757fd4460f510db528b575e0fa0d',
        redirect_uri: location.origin + '/login/social/kakao/callback',
        state: document.querySelector('input[name=csrfmiddlewaretoken]').value
    }
    url = buildUrl('https://kauth.kakao.com/oauth/authorize', params)
    location.replace(url)
}

function googleLogin(){ // 구글 로그인
    params = {
        response_type: 'code',
        client_id: '24302309163-58kin7d8rn88pb8tj8k07srg71cgg9fg.apps.googleusercontent.com',
        redirect_uri: location.origin + '/login/social/google/callback',
        state: document.querySelector('input[name=csrfmiddlewaretoken]').value,
        scope: 'openid'
    }
    url = buildUrl('https://accounts.google.com/o/oauth2/v2/auth', params)
    location.replace(url)
}

function facebookLogin(){ // 페이스북 로그인
    params = {
        response_type: 'code',
        client_id: '330925454976805',
        redirect_uri: location.origin + '/login/social/facebook/callback',
        state: document.querySelector('input[name=csrfmiddlewaretoken]').value
    }
    url = buildUrl('https://www.facebook.com/v7.0/dialog/oauth', params)
    location.replace(url)
}
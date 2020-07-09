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
        redirect_url: location.origin + '/login/social/naver/callback/',
        state: document.querySelector('input[name=csrfmiddlewaretoken]').value
    }
    url = buildUrl('https://nid.naver.com/oauth2.0/authorize', params)
    location.replace(url)
}
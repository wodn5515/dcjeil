function getCookie(name){
    if(document.cookie){
        let cookiesArr = document.cookie.split("; ");
        for(let i = 0; i<cookiesArr.length; i++){
            let cookie = cookiesArr[i].split('=');
            if(cookie[0]==name){
                return cookie[1];
            }
        }
    }
    return false;
}

function setCookieAt00(name, value){
    let todaydate = new Date();
    todaydate = new Date(parseInt(todaydate.getTime()/86400000)*86400000 + 54000000);
    if(getCookie(name)){
        document.cookie = name + "=" + getCookie(name) + "|" + escape(value) + "; path=/; expires=" + todaydate.toUTCString(); + ";";
    }else{
        document.cookie = name + "=" + escape(value) + "; path=/; expires=" + todaydate.toUTCString(); + ";";
    }
}
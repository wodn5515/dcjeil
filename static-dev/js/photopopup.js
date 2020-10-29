function onclickImage(url){
    let photoWin = window.open(url)
}

let el = document.querySelector("#detail_content")
let imageList = el.querySelectorAll("p > img")

for(let i = 0; i < imageList.length; i++){
    imageList[i].addEventListener('click', function() {
        onclickImage(imageList[i].src);
    });
}


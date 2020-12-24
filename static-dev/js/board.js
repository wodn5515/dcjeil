function historyDecade(number){
    let table = document.querySelector('.history_table.on');
    let btn = document.querySelector('.decade_btn.on');
    table.classList.remove('on');
    btn.classList.remove('on');
    table = document.querySelector('.tb'+number);
    btn = document.querySelector('.decade'+number);
    table.classList.add('on');
    btn.classList.add('on');
}
    let textblock = document.getElementsByClassName('Slider-text');
    let dlinna = 100;
    let Vals = [];
    for (let i=0;i<textblock.length;i++){
        if(textblock[i].innerText.length > dlinna){
            Vals[i] = textblock[i].innerText;
            textblock[i].innerText = textblock[i].innerText.substr(0 , dlinna) + '...';
        }
    }

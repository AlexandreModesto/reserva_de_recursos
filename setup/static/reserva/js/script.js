    setTimeout(() => {
    $("#messageDiv").fadeOut("slow");},2500);

    const preloaderWrapper=document.querySelector('.preloader-wrapper');
    window.addEventListener('load', ()=>{
        preloaderWrapper.style.opacity='0';
        setTimeout(() => {
            preloaderWrapper.style.display='none';
        },200);

    });

$(document).ready(function () {
            $("#botaor").click(function (event) {
                event.preventDefault();
                document.getElementById('repro').style.display='inline';
                document.getElementById('submit').style.display='inline';
            });
        });

    function showLoadingModal(){
        loadingModal = document.getElementById('loadingModal')
        loadingModal.style.display = 'flex';
    }

    //For forms: add the class "show-loading-after-submit" to any form you want to show the loader
    var formsToDelay = document.getElementsByClassName('show-loading-after-submit');
    for (var i = 0; i < formsToDelay.length; i++) {
        formsToDelay[i].addEventListener('submit', showLoadingModal);
        }
    //For urls: add the class "show-loading-after-click" to any url (a element) you want to show the loader
    function showLoaderOnUrlClick(url) {
      showLoadingModal()
      window.location=url
  }

$(document).on('change',function () {
    var largura = window.innerWidth;
    if (document.getElementById('id_repetir').checked === true){
        if (largura < 1767){
            document.getElementById('divRepetir').style.display='inline';
            document.getElementById('divRepetir').style.visibility='visible';
        }else{document.getElementById('divRepetir').style.visibility='visible';}
    }else{
        if (largura < 1767){
            document.getElementById('divRepetir').style.display='none';
            document.getElementById('divRepetir').style.visibility='hidden';
        }else{document.getElementById('divRepetir').style.visibility='hidden';}
    }
});


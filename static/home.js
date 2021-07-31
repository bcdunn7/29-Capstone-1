// fading nav-bar


window.addEventListener('scroll', function(){
    if (!$('#headnav-div').attr('style')) {
        if(window.scrollY < 35) {
                    showHeadNav()
                }
                else if (window.scrollY > 36 && window.scrollY < 100) {
                    fadeHeadNav()
                }
    }
})


function showHeadNav() {
    // $('#headnav-div').attr('style', "opacity: 0")
    // $('#headnav-div').removeClass('d-none');
    $('#headnav-div').fadeTo(1, 1, function(){
        $('#headnav-div').removeClass('d-none');
        this.setAttribute('style', "")
    });
}


function fadeHeadNav() {
    $('#headnav-div').fadeTo(100, 0, function(){
        this.classList.add('d-none');
        this.setAttribute('style', "")
    });
}


// block btns
$('#tutorial-block-btn').on('click', function(){
    window.location = $('#tutorial-block-btn').data('location');
})
$('#simulator-block-btn').on('click', function(){
    window.location = $('#simulator-block-btn').data('location');
})
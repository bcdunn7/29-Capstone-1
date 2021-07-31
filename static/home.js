// fading nav-bar
$(document).ready(function(){
    let prevScroll = 0;

    $(window).scroll(function(){
        let currScroll = $(this).scrollTop();
        
        if (currScroll > prevScroll) {
            if (!$('#headnav-div').attr('style')) {
                    // down
                fadeHeadNav()
            }
        }
        else if (currScroll < prevScroll) {
            // up
            showHeadNav()
        }

        prevScroll = currScroll;
    })
})


function showHeadNav() {
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
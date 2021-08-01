// how-to replay btn
$('#tutorial-replay-mode-btn').on('click', function(){
    $('#mode-description-div').addClass('d-none');
    $('#two-modes-div').addClass('d-none');
    $('#tutorial-simulator-explanation').addClass('d-none');
    $('#tutorial-replay-mode-explanation').removeClass('d-none');
    $('#tutorial-back-btn').removeClass('d-none');
    $('#replay-img').removeClass('d-none');
    $('#sim-img').addClass('d-none');
})

// how-to sim btn
$('#tutorial-simulator-btn').on('click', function(){
    $('#mode-description-div').addClass('d-none');
    $('#two-modes-div').addClass('d-none');
    $('#tutorial-replay-mode-explanation').addClass('d-none');
    $('#tutorial-simulator-explanation').removeClass('d-none');
    $('#tutorial-back-btn').removeClass('d-none');
    $('#replay-img').addClass('d-none')
    $('#sim-img').removeClass('d-none')
})

// back

$('#tutorial-back-btn').on('click', function(){
    $('#mode-description-div').removeClass('d-none');
    $('#two-modes-div').removeClass('d-none');
    $('#tutorial-replay-mode-explanation').addClass('d-none');
    $('#tutorial-simulator-explanation').addClass('d-none');
    $('#tutorial-back-btn').addClass('d-none');
})
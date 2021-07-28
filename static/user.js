$('#delete-user-modal-trigger').on('click', function() {
    $('#delete-user-modal').modal('show');
})
$('#erase-data-modal-trigger').on('click', function() {
    $('#erase-data-modal').modal('show');
})

$('.modal-dismiss').on('click', function() {
    $('.modal').modal('hide');
})
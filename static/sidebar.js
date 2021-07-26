// toggle sidebar 
$('#sidebar-toggle-open').on('click', function() {
    $('#sidebar').addClass('active'); 
    $('#overlay').addClass('active');
})

$('#sidebar-toggle-close').on('click', function() {
    $('#sidebar').removeClass('active'); 
    $('#overlay').removeClass('active');
})
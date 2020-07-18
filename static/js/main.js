// Delete modal
$('#delete').on('shown.bs.modal', function () {
    $('#delete').trigger('focus')
})

// Flashed message fade out
var fade_out = function () {
    $("#msg").fadeOut().empty();
}

setTimeout(fade_out, 5000);


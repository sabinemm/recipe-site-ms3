$('#delete').on('shown.bs.modal', function () {
    $('#delete').trigger('focus')
})


var fade_out = function () {
    $("#msg").fadeOut().empty();
}

setTimeout(fade_out, 5000);


// Delete modal
$('#delete').on('shown.bs.modal', function () {
    $('#delete').trigger('focus')
})

// Flashed message fade out
var fade_out = function () {
    $("#msg").fadeOut().empty();
}

setTimeout(fade_out, 5000);

// Back to top
$(document).ready(function () {
    $("a[href='#top']").click(function () {
        $("html, body").animate({ scrollTop: 0 }, "slow");
        return false;
    });

    $(window).scroll(function () {
        if ($(this).scrollTop() > 200) {
            $('.to-top').fadeIn();
        } else {
            $('.to-top').fadeOut();
        }
    });
});
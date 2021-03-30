

/* Code from : https://stackoverflow.com/questions/35965321/flashing-message-in-flask-on-a-bootstrap-modal */

$(document).ready(function() {
    var messages = "{{ get_flashed_messages() }}";

    if (typeof messages != 'undefined' && messages != '[]') {
        $("#myModal").modal();
    };
});


$('#modalDelete').modal(options)


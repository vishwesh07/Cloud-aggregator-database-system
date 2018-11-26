$(function() {
    $('document').ready(function() {
        alert("Success");
        $.ajax({
            url: '/login',
            data: $('form').serialize(),
            type: 'GET',


            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
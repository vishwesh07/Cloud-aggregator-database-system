$(function() {
    $('document').ready(function() {
        $('#inputName').val(sessionStorage.getItem("name"));
        $('#inputEmail').val(sessionStorage.getItem("email_id"));
        $('#inputBankAccount').val(sessionStorage.getItem("bankAccount"));
        $('#inputPassword').val(sessionStorage.getItem("password"));
        $(".updateSuccess").hide();
    });

    $('#updateProfile').click(function() {
        console.log($('form').serialize());
        $.ajax({
            url: '/updateProfile?inputRole='+sessionStorage.getItem("role")+'&inputId='+sessionStorage.getItem("id"),
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                $(".updateSuccess").show();
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
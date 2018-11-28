$(function() {
    var dropdownval = "";

    $(".roleClass").click(function(e) {
        $(".roleBtnClass").text(e.target.text);
        dropdownval = e.target.text;
    });

    $('#btnSignUp').click(function() {

        $.ajax({
            url: '/signUp?inputRole='+dropdownval,
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
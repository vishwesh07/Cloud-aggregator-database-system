$(function() {
    var dropdownval = "";

    $(".roleClass").click(function(e) {
        $(".roleBtnClass").text(e.target.text);
        dropdownval = e.target.text;
    });

    $('#btnLogin').click(function() {

        $.ajax({
            url: '/login?role='+dropdownval,
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                window.location.replace("http://localhost:5000/showCustomerAccountDisplay");
            },
            error: function(error) {
                $(".errorText").text(JSON.parse(error.responseText).error);
                console.log(error);
            }
        });
    });
});
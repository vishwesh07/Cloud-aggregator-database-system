$(function() {
    var dropdownval = "";

    $(".roleClass").click(function(e) {
        $(".roleBtnClass").text(e.target.text);
        dropdownval = e.target.text;
    });

    $('#btnLogin').click(function() {
        sessionStorage.setItem("email_id", dropdownval);
        $.ajax({
            url: '/login?role='+dropdownval,
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                sessionStorage.setItem("email_id", JSON.parse(response).results[0][1]);
                sessionStorage.setItem("id", JSON.parse(response).results[0][0]);
                window.location.replace("http://localhost:5000/showCustomerAccountDisplay");
            },
            error: function(error) {
                $(".errorText").text(JSON.parse(error.responseText).error);
                console.log(error);
            }
        });
    });
});
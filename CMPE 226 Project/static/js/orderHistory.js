$(function() {
    $('document').ready(function() {
        $.ajax({
            url: '/orderHistory?customer_id='+sessionStorage.getItem("id"),
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
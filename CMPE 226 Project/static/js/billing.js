$(function() {
    $('document').ready(function() {
        $.ajax({
            url: '/bills?customer_id='+sessionStorage.getItem("id"),
            data: $('form').serialize(),
            type: 'GET',
            success: function(response) {
                console.log(response);
                var bills = JSON.parse(response).results;
                var $ul = $('.bills').append(
                  bills.map(bill =>
                    $("<tr>").append($("<td>").text(bill[0])).append($("<td>").text(bill[1]))
                        .append($("<td>").text(bill[5])).append($("<td>").text(bill[6])).append($("<td>").text(bill[7]))
                  )
                );
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
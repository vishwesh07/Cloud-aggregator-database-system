$(function() {
    $('document').ready(function() {
        $.ajax({
            url: '/orderHistory?customer_id='+sessionStorage.getItem("id"),
            type: 'GET',
            success: function(response) {
                var orderList = JSON.parse(response).results;
                var $ul = $('.orderHistory').append(
                  orderList.map(order =>
                    $("<tr>").append($("<td>").text(order[0]))
                        .append($("<td>").text(order[1])).append($("<td>").text(order[2]))
                        .append($("<td>").text(order[5])).append($("<td>").text(order[6]))
                        .append($("<td>").text(order[7])).append($("<td>").text(order[8]))
                        .append($("<td>").text(order[9]))
                  )
                );
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
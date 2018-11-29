$(function() {
    $('.placeOrder').click(function() {
        console.log($('.placeOrderForm').serialize());
        $.ajax({
            url: '/placeOrder?customer_id='+sessionStorage.getItem("id"),
            data: $('.placeOrderForm').serialize(),
            type: 'POST',
            success: function(response) {
                var orderList = JSON.parse(response).results;
                var $ul = $('.currentOrders').append(
                  orderList.map(order =>
                    $("<tr>").append($("<td>").text(order[0]))
                        .append($("<td>").text(order[1])).append($("<td>").text(order[2]))
                        .append($("<td>").text(order[5])).append($("<td>").text(order[6]))
                        .append($("<td>").text(order[7])).append($("<td>").text(order[8]))
                  )
                );
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    $('document').ready(function() {
        $.ajax({
            url: '/currentOrders?customer_id='+sessionStorage.getItem("id"),
            type: 'GET',
            success: function(response) {
                var orderList = JSON.parse(response).results;
                var $ul = $('.currentOrders').append(
                  orderList.map(order =>
                    $("<tr>").append($("<td>").text(order[0]))
                        .append($("<td>").text(order[1])).append($("<td>").text(order[2]))
                        .append($("<td>").text(order[5])).append($("<td>").text(order[6]))
                        .append($("<td>").text(order[7])).append($("<td>").text(order[8]))
                  )
                );
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
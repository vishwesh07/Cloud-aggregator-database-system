$(function() {
    $('document').ready(function() {
        $.ajax({
            url: '/getOffer?inputId='+sessionStorage.getItem("id")+'&inputCaId='+sessionStorage.getItem("ca_id")+'&inputRole='+sessionStorage.getItem("role"),
            type: 'GET',
            success: function(response) {
                var orderList = JSON.parse(response).results;
                var $ul = $('.currentOrders').append(
                  orderList.map(order =>
                    $("<tr>").append($("<td>").text(order[0]))
                        .append($("<td>").text(order[1])).append($("<td>").text(order[2]))
                        .append($("<td>").append($('<button type="button" class="btn-sm btn-danger">Delete</button>')))
                  )
                );
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
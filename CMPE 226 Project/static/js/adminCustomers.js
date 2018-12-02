$(function() {
    $('document').ready(function() {
        $.ajax({
            url: '/myCustomers?inputCaId='+sessionStorage.getItem("ca_id")+'&inputRole='+sessionStorage.getItem("role"),
            type: 'GET',
            success: function(response) {
                var orderList = JSON.parse(response).results;
                var $ul = $('.currentOrders').append(
                  orderList.map(order =>
                      $("<tr>").append($("<td>").text(order[0]))
                          .append($("<td>").text(order[1])).append($("<td>").text(order[2]))
                          .append($("<td>").text(order[4])).append($("<td>").text(order[5]))
                          .append($("<td>").append($('<button type="button" class="btn-sm btn-danger">Delete</button>')))
                          .append($("<td>").append(order[6]).append($('<button type="button" class="btn-sm btn-info">Update</button>')))
                  )
                );
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
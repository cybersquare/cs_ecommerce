function delete_product(id) {
    var del_id = id;
    console.log("idididid", del_id + 1)
    $.ajax({
        url: 'deleteProducts',
        type: 'GET',
        // processData: false,
        // contentType: false,
        data: {
            'id': del_id
        },

        success: function(response) {

            toastr.success(response.msg);


        },
        error: function(response) {

            toastr.success(response.msg);


        }

    });
}
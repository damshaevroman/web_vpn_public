//logout from app
    $("#logout").click(function() {
        $.ajax({
            url: "/logout/",
            // data: serdata,
            type: 'GET',
            success: function(response) {
                console.log("Logout")
            },
            error: function (response) {
                console.log("Logout Error")
            }
        });
    });